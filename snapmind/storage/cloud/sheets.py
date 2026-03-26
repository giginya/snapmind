import gspread
from google.oauth2.service_account import Credentials
import streamlit as st


# 🔷 SCOPES (required for Sheets + Drive)
SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive",
]


def connect_sheet():
    """
    Establish connection to Google Sheets using Streamlit secrets.
    Returns the first worksheet.
    """

    try:
        creds_dict = st.secrets["gcp_service_account"]

        credentials = Credentials.from_service_account_info(
            creds_dict,
            scopes=SCOPES
        )

        client = gspread.authorize(credentials)

        sheet_name = st.secrets["SHEET_NAME"]

        sheet = client.open(sheet_name).sheet1

        return sheet

    except Exception as e:
        raise RuntimeError(f"Failed to connect to Google Sheets: {e}")
