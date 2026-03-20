import streamlit as st
import os
from processor_pipeline import process_image

# ------------------------------------------------------------
# PAGE CONFIG
# ------------------------------------------------------------
st.set_page_config(page_title="SnapMind", layout="centered")

st.title("📸 SnapMind")
st.write("Turn screenshots into usable knowledge")

# ------------------------------------------------------------
# UPLOAD IMAGE
# ------------------------------------------------------------
uploaded_file = st.file_uploader(
    "Upload Screenshot",
    type=["png", "jpg", "jpeg"]
)

if uploaded_file:

    os.makedirs("uploads", exist_ok=True)

    file_path = os.path.join("uploads", uploaded_file.name)

    # Save uploaded file
    with open(file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())

    st.info("Processing image...")

    result = process_image(file_path)

    if result:
        st.success("Done!")
        st.text_area("Extracted Text", result, height=200)
    else:
        st.warning("No text detected")

# ------------------------------------------------------------
# DISPLAY SAVED NOTES
# ------------------------------------------------------------
if os.path.exists("notes"):
    st.subheader("🧠 Saved Notes")

    files = sorted(os.listdir("notes"), reverse=True)

    for file in files[:5]:
        with open(os.path.join("notes", file)) as f:
            st.text(f.read())
