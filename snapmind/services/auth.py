import random
import datetime

from snapmind.utils.validators import is_valid_email, is_valid_otp


# simple in-memory user store (upgrade later)
USERS = {}


def generate_otp(length: int = 6) -> str:
    return "".join([str(random.randint(0, 9)) for _ in range(length)])


def is_otp_expired(expiry: str) -> bool:
    return datetime.datetime.utcnow() > datetime.datetime.fromisoformat(expiry)


def register_user(email: str):
    if not is_valid_email(email):
        return False

    otp = generate_otp()
    expiry = str(datetime.datetime.utcnow() + datetime.timedelta(minutes=5))

    USERS[email] = {
        "otp": otp,
        "expiry": expiry,
        "verified": False
    }

    print(f"[DEBUG OTP] {email}: {otp}")  # replace with email sender later

    return True


def verify_otp(email: str, otp: str) -> bool:
    if email not in USERS:
        return False

    if not is_valid_otp(otp):
        return False

    user = USERS[email]

    if is_otp_expired(user["expiry"]):
        return False

    if user["otp"] != otp:
        return False

    user["verified"] = True
    return True
