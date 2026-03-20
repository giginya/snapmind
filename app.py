import streamlit as st
import os
from datetime import datetime

from processor_pipeline import process_image

# ------------------------------------------------------------
# CONFIG
# ------------------------------------------------------------
st.set_page_config(page_title="SnapMind", layout="centered")

# ------------------------------------------------------------
# GOOGLE SHEETS CONNECTION (SAFE + CLEAN)
# ------------------------------------------------------------


def connect_sheet():
    try:
        import gspread
        from google.oauth2.service_account import Credentials
    except Exception:
        raise Exception("Google Sheets dependencies not installed")

    if "gcp_service_account" not in st.secrets:
        raise Exception("Missing Streamlit secrets (gcp_service_account)")

    scope = [
        "https://www.googleapis.com/auth/spreadsheets",
        "https://www.googleapis.com/auth/drive"
    ]

    try:
        creds = Credentials.from_service_account_info(
            st.secrets["gcp_service_account"],
            scopes=scope
        )

        client = gspread.authorize(creds)
        sheet = client.open("SnapMind Users").sheet1

        return sheet

    except Exception as e:
        raise Exception(f"Google Sheets connection failed: {e}")


def save_user(email):
    try:
        sheet = connect_sheet()
        sheet.append_row([email, str(datetime.now())])
    except Exception as e:
        st.warning("⚠️ Could not save to database (continuing anyway)")
        st.text(f"Details: {e}")


# ------------------------------------------------------------
# SESSION STATE
# ------------------------------------------------------------
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "last_result" not in st.session_state:
    st.session_state.last_result = None

# ------------------------------------------------------------
# LOGIN FORM (MAIN SCREEN)
# ------------------------------------------------------------
if not st.session_state.logged_in:

    st.title("🔐 SnapMind Login")

    with st.form("login_form"):
        email = st.text_input("Email")
        password = st.text_input("Password", type="password")

        submitted = st.form_submit_button("Login")

        if submitted:
            if email and password:
                save_user(email)
                st.session_state.logged_in = True
                st.success("Welcome!")
                st.rerun()
            else:
                st.error("Please enter email and password")

    st.stop()

# ------------------------------------------------------------
# MAIN APP
# ------------------------------------------------------------
st.title("📸 SnapMind")
st.write("Turn screenshots into usable knowledge")

uploaded_file = st.file_uploader(
    "Upload Screenshot",
    type=["png", "jpg", "jpeg"]
)

MAX_SIZE_MB = 5

if uploaded_file:

    if uploaded_file.size > MAX_SIZE_MB * 1024 * 1024:
        st.error("File too large (max 5MB)")
        st.stop()

    os.makedirs("uploads", exist_ok=True)
    file_path = os.path.join("uploads", uploaded_file.name)

    try:
        with open(file_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
    except Exception as e:
        st.error(f"File save error: {e}")
        st.stop()

    st.info("Processing image...")

    try:
        result = process_image(file_path)
    except Exception as e:
        st.error(f"Processing error: {e}")
        result = None

    if result:
        st.session_state.last_result = result
        st.success("Text extracted")
    else:
        st.session_state.last_result = None
        st.warning("No readable text found")

# ------------------------------------------------------------
# DISPLAY RESULT
# ------------------------------------------------------------
if st.session_state.last_result:

    edited_text = st.text_area(
        "Edit before saving",
        st.session_state.last_result,
        height=200
    )

    st.download_button(
        "💾 Download Note",
        edited_text,
        "snapmind_note.txt"
    )

# ------------------------------------------------------------
# CLEAR BUTTON
# ------------------------------------------------------------
if st.button("🧹 Clear Screen"):
    st.session_state.last_result = None
    st.rerun()
