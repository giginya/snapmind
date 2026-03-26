import gspread
from google.oauth2.service_account import Credentials
import streamlit as st
from datetime import datetime


# 🔷 SCOPES
SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive",
]


# 🔷 CONNECT

def connect_sheet():
    try:
        creds_dict = st.secrets["gcp_service_account"]

        credentials = Credentials.from_service_account_info(
            creds_dict,
            scopes=SCOPES
        )

        client = gspread.authorize(credentials)

        sheet_name = st.secrets["SHEET_NAME"]

        return client.open(sheet_name).sheet1

    except Exception as e:
        raise RuntimeError(f"Google Sheets connection failed: {e}")


# 🔷 PUSH NOTE (REQUIRED BY sync.py)

def push_note_to_sheets(email: str, note):
    """
    Stores minimal metadata about a note in Google Sheets.
    This is lightweight logging, not full storage.
    """

    sheet = connect_sheet()

    try:
        sheet.append_row([
            note.id,
            email,
            note.title,
            note.summary,
            getattr(note.metadata, "confidence", 0),
            datetime.utcnow().isoformat()
        ])
    except Exception as e:
        print("SHEETS WRITE ERROR:", e)
