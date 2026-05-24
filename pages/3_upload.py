"""
Upload a JD PDF → save to user's folder → ready for pipeline.
"""

import streamlit as st
import os, sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

st.set_page_config(page_title="Upload JD", layout="centered")

# ── Guard ─────────────────────────────────────────────────────────────────────
if "user_id" not in st.session_state:
    st.switch_page("pages/1_login.py")

user_name   = st.session_state["user_name"]
user_folder = os.path.join("user", user_name.replace(" ", "_"), "uploads")
os.makedirs(user_folder, exist_ok=True)

st.title("Upload Job Description")
st.write("Upload the JD PDF for the role you want to apply for.")
st.write("---")

uploaded_file = st.file_uploader("Choose a PDF file", type=["pdf"])

if uploaded_file:
    save_path = os.path.join("user", user_name.replace(" ", "_"), "uploads", uploaded_file.name)
    print(f"Saving uploaded file to: {save_path}")  # Debug print
    with open(save_path, "wb") as f:
        f.write(uploaded_file.getbuffer())

    st.success(f"Saved: {uploaded_file.name}")
    st.session_state["jd_path"] = save_path

    st.write("---")
    if st.button("Build My Resume →", use_container_width=True):
        progress_box = st.empty()

        try:
            progress_box.info("Stage 1/6 — Parsing JD PDF...")

            from main_pipeline import main_pipeline

            pdf_path = main_pipeline(
                path=save_path,
                user_id=st.session_state["user_id"],
                user_name=st.session_state["user_name"],
                progress_box=progress_box
            )

            progress_box.success("Resume generated successfully!")

            with open(pdf_path, "rb") as f:
                st.download_button(
                    label="Download Resume PDF",
                    data=f,
                    file_name="resume.pdf",
                    mime="application/pdf",
                )

        except Exception as e:
            progress_box.error(f"Pipeline failed: {e}")

st.write(" ")
if st.button("← Back to Profile", use_container_width=False):
    st.switch_page("pages/2_profile.py")