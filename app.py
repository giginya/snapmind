import streamlit as st
import os
import tempfile
import hashlib
from datetime import datetime

from processor_pipeline import process_image

# ------------------------------------------------------------
# CONFIG
# ------------------------------------------------------------
st.set_page_config(page_title="SnapMind", layout="wide")

# ------------------------------------------------------------
# SECURITY
# ------------------------------------------------------------


def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# ------------------------------------------------------------
# GOOGLE SHEETS (CACHED)
# ------------------------------------------------------------


@st.cache_resource
def get_gspread_client():
    import gspread
    from google.oauth2.service_account import Credentials

    scope = [
        "https://www.googleapis.com/auth/spreadsheets",
        "https://www.googleapis.com/auth/drive"
    ]

    creds = Credentials.from_service_account_info(
        st.secrets["gcp_service_account"],
        scopes=scope
    )

    return gspread.authorize(creds)


def get_user_sheet():
    return get_gspread_client().open("SnapMind Users").sheet1


def get_analytics_sheet():
    return get_gspread_client().open("SnapMind Users").worksheet("SnapMind Analytics")


# ------------------------------------------------------------
# ANALYTICS (SAFE - NEVER BREAK APP)
# ------------------------------------------------------------
def log_event(event, email="", metadata=""):
    try:
        sheet = get_analytics_sheet()
        sheet.append_row([
            str(event),
            str(email),
            str(metadata),
            str(datetime.now())
        ])
    except Exception as e:
        print("Analytics error:", e)


# ------------------------------------------------------------
# SAFE DATA ACCESS
# ------------------------------------------------------------
def safe_get_records():
    try:
        return get_user_sheet().get_all_records()
    except Exception as e:
        st.warning("Database connection failed")
        st.text(str(e))
        return []


# ------------------------------------------------------------
# USER MANAGEMENT
# ------------------------------------------------------------
def user_exists(email):
    return any(str(u.get("Email")) == str(email) for u in safe_get_records())


def verify_user(email, password):
    hashed = hash_password(password)

    for u in safe_get_records():
        if (
            str(u.get("Email")) == str(email)
            and str(u.get("PasswordHash")) == hashed
        ):
            return True

    return False


def create_user(email, password):
    try:
        get_user_sheet().append_row([
            str(email),
            hash_password(password),
            "",
            str(datetime.now())
        ])
        log_event("signup", email)
    except Exception as e:
        st.error("Signup failed")
        st.text(str(e))


# ------------------------------------------------------------
# NOTES
# ------------------------------------------------------------
def save_note(email, note):
    try:
        get_user_sheet().append_row([
            str(email),
            "",
            str(note),
            str(datetime.now())
        ])
        log_event("save_note", email)
    except Exception as e:
        st.error("Save failed")
        st.text(str(e))


def get_user_notes(email):
    records = safe_get_records()

    return [
        r for r in records
        if str(r.get("Email")) == str(email)
        and str(r.get("Note", "")).strip() != ""
    ]


# ------------------------------------------------------------
# SESSION STATE
# ------------------------------------------------------------
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "user_email" not in st.session_state:
    st.session_state.user_email = None

if "last_result" not in st.session_state:
    st.session_state.last_result = None


# ------------------------------------------------------------
# AUTH UI
# ------------------------------------------------------------
if not st.session_state.logged_in:

    st.title("🔐 SnapMind")

    tab1, tab2 = st.tabs(["Login", "Sign Up"])

    with tab1:
        email = st.text_input("Email", key="login_email")
        password = st.text_input("Password", type="password", key="login_pass")

        if st.button("Login"):
            if verify_user(email, password):
                st.session_state.logged_in = True
                st.session_state.user_email = email
                log_event("login", email)
                st.success("Logged in!")
                st.rerun()
            else:
                st.error("Invalid credentials")

    with tab2:
        email = st.text_input("Email", key="signup_email")
        password = st.text_input(
            "Password", type="password", key="signup_pass")

        if st.button("Create Account"):
            if user_exists(email):
                st.warning("User already exists")
            else:
                create_user(email, password)
                st.success("Account created")

    st.stop()


# ------------------------------------------------------------
# MAIN APP
# ------------------------------------------------------------
st.title("📸 SnapMind")
st.caption(f"Logged in as: {st.session_state.user_email}")

col1, col2 = st.columns([2, 1])

# ------------------------------------------------------------
# LEFT: UPLOAD
# ------------------------------------------------------------
with col1:

    st.subheader("Upload Screenshot")

    uploaded_file = st.file_uploader(
        "Upload Screenshot",
        type=["png", "jpg", "jpeg"]
    )

    if uploaded_file:

        log_event("upload", st.session_state.user_email, uploaded_file.name)

        st.info("Processing...")

        temp_path = None

        try:
            with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as tmp:
                tmp.write(uploaded_file.getbuffer())
                temp_path = tmp.name

            result = process_image(temp_path)

        except Exception as e:
            st.error(f"Processing error: {e}")
            log_event("process_failed", st.session_state.user_email)
            result = None

        finally:
            if temp_path and os.path.exists(temp_path):
                try:
                    os.remove(temp_path)
                except:
                    pass

        if result:
            st.session_state.last_result = result
            log_event("process_success", st.session_state.user_email)
            st.success("Done")
        else:
            st.warning("No text found")

    if st.session_state.last_result:

        edited = st.text_area(
            "Edit Note",
            st.session_state.last_result,
            height=200
        )

        if st.button("💾 Save Note"):
            save_note(st.session_state.user_email, edited)
            st.success("Saved!")


# ------------------------------------------------------------
# RIGHT: USER HISTORY
# ------------------------------------------------------------
with col2:

    st.subheader("📚 Your Notes")

    notes = get_user_notes(st.session_state.user_email)

    if not notes:
        st.info("No notes yet")
    else:
        for n in reversed(notes[-10:]):

            timestamp = str(n.get("Timestamp", "No timestamp"))
            note = str(n.get("Note", ""))

            label: str = f"{timestamp}"

            with st.expander(label):
                st.write(note)


# ------------------------------------------------------------
# FOOTER
# ------------------------------------------------------------
st.markdown("---")

if st.button("🚪 Logout"):
    st.session_state.logged_in = False
    st.session_state.user_email = None
    st.rerun()
