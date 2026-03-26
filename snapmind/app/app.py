import streamlit as st

from snapmind.core.pipeline import run_pipeline
from snapmind.services.sync import save_and_sync
from snapmind.services.auth import register_user, verify_otp
from snapmind.services.analytics import track_event
from snapmind.ml.feedback import log_feedback


# 🔷 App State

if "authenticated" not in st.session_state:
    st.session_state["authenticated"] = False

if "email" not in st.session_state:
    st.session_state["email"] = ""


# 🔷 AUTH FLOW

if not st.session_state["authenticated"]:

    st.title("SnapMind — Login")

    email = st.text_input("Enter your email")

    if st.button("Send Code"):
        if register_user(email):
            st.session_state["email"] = email
            st.success("Code sent (check console)")
        else:
            st.error("Invalid email")

    otp = st.text_input("Enter OTP")

    if st.button("Verify"):
        if verify_otp(st.session_state["email"], otp):
            st.session_state["authenticated"] = True
            st.success("Authenticated")
        else:
            st.error("Invalid or expired OTP")

    st.stop()


# 🔷 MAIN APP

st.title("SnapMind v2.1")

uploaded_file = st.file_uploader("Upload Image")

if uploaded_file:

    with st.spinner("Processing..."):
        note = run_pipeline(uploaded_file)

    st.subheader(note.title)
    st.write(note.summary)

    st.write("### Blocks")
    for b in note.blocks:
        st.write(f"- {b.content}")

    st.write(f"Confidence: {note.metadata.confidence:.2f}")

    # 🔷 EDITING
    edited_summary = st.text_area("Edit Summary", value=note.summary)

    if st.button("Save Note"):
        note.summary = edited_summary

        save_and_sync(note)

        # 🔥 feedback logging
        log_feedback(
            {"summary": note.summary},
            {"summary": edited_summary}
        )

        track_event("note_saved", st.session_state["email"])

        st.success("Saved successfully")
