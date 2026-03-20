import streamlit as st
import os
from processor_pipeline import process_image

# ------------------------------------------------------------
# CONFIG
# ------------------------------------------------------------
st.set_page_config(page_title="SnapMind", layout="centered")

# ------------------------------------------------------------
# BASIC ACCESS CONTROL (TEMP SECURITY)
# ------------------------------------------------------------
PASSWORD = "snapmind123"

if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

if not st.session_state.authenticated:
    pwd = st.text_input("Enter access password", type="password")

    if pwd == PASSWORD:
        st.session_state.authenticated = True
        st.rerun()
    else:
        st.stop()

# ------------------------------------------------------------
# SESSION STATE (PREVENT STACKING)
# ------------------------------------------------------------
if "last_result" not in st.session_state:
    st.session_state.last_result = None

# ------------------------------------------------------------
# UI
# ------------------------------------------------------------
st.title("📸 SnapMind")
st.write("Turn screenshots into usable knowledge")

# ------------------------------------------------------------
# FILE UPLOAD
# ------------------------------------------------------------
uploaded_file = st.file_uploader(
    "Upload Screenshot",
    type=["png", "jpg", "jpeg"]
)

MAX_SIZE_MB = 5

if uploaded_file:

    # FILE SIZE LIMIT
    if uploaded_file.size > MAX_SIZE_MB * 1024 * 1024:
        st.error("File too large. Max 5MB allowed.")
        st.stop()

    os.makedirs("uploads", exist_ok=True)

    file_path = os.path.join("uploads", uploaded_file.name)

    with open(file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())

    st.info("Processing image...")

    result = process_image(file_path)

    if result:
        st.session_state.last_result = result
        st.success("Text extracted successfully")

    else:
        st.session_state.last_result = None
        st.warning("⚠️ No readable text found in this image")

# ------------------------------------------------------------
# DISPLAY RESULT
# ------------------------------------------------------------
if st.session_state.last_result:

    st.subheader("🧠 Extracted Text")

    edited_text = st.text_area(
        "Edit before saving",
        st.session_state.last_result,
        height=200
    )

    # DOWNLOAD BUTTON
    st.download_button(
        label="💾 Download Note",
        data=edited_text,
        file_name="snapmind_note.txt",
        mime="text/plain"
    )

# ------------------------------------------------------------
# CLEAR BUTTON
# ------------------------------------------------------------
if st.button("🧹 Clear Screen"):
    st.session_state.last_result = None
    st.rerun()
