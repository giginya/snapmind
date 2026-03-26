import random
import datetime
import hashlib
import smtplib
from email.mime.text import MIMEText

from altair import value
import streamlit as st

from snapmind.utils.validators import is_valid_email, is_valid_otp
from snapmind.storage.cloud import sheets


# 🔷 CONFIG
OTP_EXPIRY_MINUTES = 5
OTP_RESEND_COOLDOWN_SECONDS = 60


# 🔷 UTILITIES

def generate_otp(length: int = 6) -> str:
    return "".join(str(random.randint(0, 9)) for _ in range(length))


def hash_otp(otp: str) -> str:
    return hashlib.sha256(otp.encode()).hexdigest()


def now_utc():
    return datetime.datetime.utcnow()


# 🔷 EMAIL

def send_otp_email(email: str, otp: str) -> bool:
    try:
        sender = st.secrets["EMAIL_SENDER"]
        password = st.secrets["EMAIL_PASSWORD"]

        msg = MIMEText(f"""
Your SnapMind verification code is:

{otp}

Expires in {OTP_EXPIRY_MINUTES} minutes.
""")

        msg["Subject"] = "SnapMind OTP"
        msg["From"] = sender
        msg["To"] = email

        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(sender, password)
            server.sendmail(sender, email, msg.as_string())

        return True

    except Exception as e:
        print("EMAIL ERROR:", e)
        return False


# 🔷 SHEETS HELPERS

def get_all_records():
    sheet = sheets.connect_sheet()
    return sheet, sheet.get_all_records()


def get_user_record(email: str):
    _, records = get_all_records()

    for r in records:
        if str(r["email"]) == email:
            return r

    return None


def upsert_user(email: str, otp_hash: str, expiry: str):
    sheet, records = get_all_records()

    for i, r in enumerate(records):
        if str(r["email"]) == email:
            row_index = i + 2

            sheet.update(
                range_name=f"C{row_index}:E{row_index}",
                values=[[otp_hash, expiry, "false"]]
            )
            return

    sheet.append_row([
        email,
        now_utc().isoformat(),
        otp_hash,
        expiry,
        "false"
    ])


def mark_verified(email: str):
    sheet, records = get_all_records()

    for i, r in enumerate(records):
        if str(r["email"]) == email:
            row_index = i + 2

            sheet.update(
                range_name=f"E{row_index}",
                values=[["true"]]
            )
            return


# 🔷 REGISTER

def register_user(email: str) -> bool:

    if not is_valid_email(email):
        return False

    record = get_user_record(email)

    # 🔴 RATE LIMIT

    def parse_datetime_safe(value):
        """
        Safely parse datetime from Google Sheets.
        Handles string, float, empty, and invalid values.
        """

        import datetime

        # Case 1: Already valid ISO string
        try:
            return datetime.datetime.fromisoformat(str(value))
        except Exception:
            pass

        # Case 2: Excel / Sheets numeric timestamp
        try:
            # Excel epoch starts 1899-12-30
            excel_epoch = datetime.datetime(1899, 12, 30)
            return excel_epoch + datetime.timedelta(days=float(value))
        except Exception:
            pass

        # Case 3: fallback (treat as old → allow resend)
        return datetime.datetime.utcnow() - datetime.timedelta(hours=1)

    # 🔷 RATE LIMIT CHECK (SAFE VERSION)

    if record:
        last_time = parse_datetime_safe(record.get("created_at"))

        time_diff = (now_utc() - last_time).total_seconds()

        # 🔍 Debug visibility (VERY IMPORTANT)
        print("RATE CHECK:")
        print("last_time:", last_time)
        print("now:", now_utc())
        print("diff (seconds):", time_diff)

        if time_diff < OTP_RESEND_COOLDOWN_SECONDS:
            print("⛔ RATE LIMITED")
            return False

        otp = generate_otp()
        otp_hash = hash_otp(otp)

        expiry = (now_utc() + datetime.timedelta(
            minutes=OTP_EXPIRY_MINUTES
        )).isoformat()

        upsert_user(email, otp_hash, expiry)

        return send_otp_email(email, otp)

    return False


# 🔷 VERIFY

def verify_otp(email: str, otp: str) -> bool:

    if not is_valid_otp(otp):
        return False

    record = get_user_record(email)

    if not record:
        return False

    expiry = datetime.datetime.fromisoformat(
        str(record["expiry"])
    )

    if now_utc() > expiry:
        return False

    otp_hash = hash_otp(otp)

    if otp_hash != str(record["otp_hash"]):
        return False

    mark_verified(email)
    return True
