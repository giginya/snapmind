import streamlit as st

from snapmind.core.pipeline import run_pipeline
from snapmind.services.sync import save_and_sync
from snapmind.services.auth import register_user, verify_otp
from snapmind.services.analytics import track_event
from snapmind.ml.feedback import log_feedback


# 🔷 SESSION STATE INITIALIZATION

if "authenticated" not in st.session_state:
    st.session_state["authenticated"] = False

if "auth_state" not in st.session_state:
    st.session_state["auth_state"] = "email"

if "email" not in st.session_state:
    st.session_state["email"] = ""


# 🔴 AUTH FLOW

if not st.session_state["authenticated"]:

    st.set_page_config(page_title="SnapMind", layout="centered")

    st.title("SnapMind")

    st.markdown("""
### Turn screenshots into usable knowledge

Stop saving screenshots you never use.  
SnapMind converts them into structured, searchable insights in seconds.
""")

    # 🔵 STATE: EMAIL INPUT
    if st.session_state["auth_state"] == "email":

        email = st.text_input("Enter your email",
                              placeholder="you@example.com")

        if st.button("Get Access"):

            if not email:
                st.warning("Please enter your email")
                st.stop()

            with st.spinner("Sending verification code..."):
                success = register_user(email)

            if success:
                st.session_state["email"] = email
                st.session_state["auth_state"] = "otp"

                st.success("📩 Code sent. Check your inbox (and spam folder).")

                track_event("otp_requested", email)

                st.rerun()

            else:
                st.error("Unable to send code. Try again in a moment.")

    # 🔵 STATE: OTP INPUT
    elif st.session_state["auth_state"] == "otp":

        st.info(f"""
A verification code has been sent to:

**{st.session_state['email']}**

Enter the code below to continue.
""")

        otp = st.text_input("Enter 6-digit code")

        col1, col2 = st.columns(2)

        # 🔷 VERIFY
        with col1:
            if st.button("Verify Code"):

                with st.spinner("Verifying..."):

                    if verify_otp(st.session_state["email"], otp):
                        st.session_state["authenticated"] = True

                        track_event("otp_verified", st.session_state["email"])

                        st.success("✅ You're in")

                        st.rerun()
                    else:
                        st.error("Invalid or expired code")

        # 🔷 RESEND
        with col2:
            if st.button("Resend Code"):

                with st.spinner("Sending new code..."):

                    success = register_user(st.session_state["email"])

                if success:
                    st.success("New code sent")
                    track_event("otp_resent", st.session_state["email"])
                else:
                    st.warning("Please wait before requesting another code")

    st.stop()


# 🔴 MAIN APP (POST-AUTH)

st.set_page_config(page_title="SnapMind", layout="wide")

st.title("SnapMind")

st.caption(f"Logged in as {st.session_state['email']}")

st.markdown("### Upload a screenshot")

uploaded_file = st.file_uploader(
    "Drop an image or click to upload",
    type=["png", "jpg", "jpeg"]
)

if uploaded_file:

    with st.spinner("Processing your screenshot..."):
        note = run_pipeline(uploaded_file)

    st.success("Processed successfully")

    # 🔷 DISPLAY RESULT
    st.subheader(note.title)
    st.write(note.summary)

    st.markdown("### Key Points")

    for b in note.blocks:
        st.write(f"- {b.content}")

    st.caption(f"Confidence: {note.metadata.confidence:.2f}")

    # 🔷 EDITING
    st.markdown("### Refine your note")

    edited_summary = st.text_area(
        "Edit summary",
        value=note.summary
    )

    if st.button("Save Note"):

        note.summary = edited_summary

        save_and_sync(note)

        log_feedback(
            {"summary": note.summary},
            {"summary": edited_summary}
        )

        track_event("note_saved", st.session_state["email"])

        st.success("Saved successfully")
