import streamlit as st
import os
from processor_pipeline import process_image

st.set_page_config(page_title="SnapMind", layout="centered")

st.title("📸 SnapMind")
st.write("Turn screenshots into usable knowledge")

# ------------------------------------------------------------
# SESSION STATE (PREVENT STACKING)
# ------------------------------------------------------------
if "last_result" not in st.session_state:
    st.session_state.last_result = None

# ------------------------------------------------------------
# UPLOAD
# ------------------------------------------------------------
uploaded_file = st.file_uploader(
    "Upload Screenshot",
    type=["png", "jpg", "jpeg"]
)

if uploaded_file:

    os.makedirs("uploads", exist_ok=True)

    file_path = os.path.join("uploads", uploaded_file.name)

    with open(file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())

    st.info("Processing...")

    result = process_image(file_path)

    if result:
        st.session_state.last_result = result
        st.success("Text extracted successfully")

    else:
        st.session_state.last_result = None
        st.warning("⚠️ No readable text found in this image")

# ------------------------------------------------------------
# DISPLAY RESULT (ONLY LAST RESULT)
# ------------------------------------------------------------
if st.session_state.last_result:

    st.subheader("🧠 Extracted Text")

    st.text_area(
        "Edit before saving",
        st.session_state.last_result,
        height=200,
        key="editable_text"
    )

    # --------------------------------------------------------
    # DOWNLOAD BUTTON (SAVE FEATURE)
    # --------------------------------------------------------
    st.download_button(
        label="💾 Download Note",
        data=st.session_state.last_result,
        file_name="snapmind_note.txt",
        mime="text/plain"
    )

# ------------------------------------------------------------
# CLEAR BUTTON (CRITICAL UX FIX)
# ------------------------------------------------------------
if st.button("🧹 Clear Screen"):
    st.session_state.last_result = None
    st.rerun()
