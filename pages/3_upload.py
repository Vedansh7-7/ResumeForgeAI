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
    save_path = os.path.join(user_folder, uploaded_file.name)

    with open(save_path, "wb") as f:
        f.write(uploaded_file.getbuffer())

    st.success(f"Saved: {uploaded_file.name}")
    st.session_state["jd_path"] = save_path

    st.write("---")
    if st.button("Build My Resume →", use_container_width=True):
        # TODO: call pipeline here
        # from resume_platform.pipeline import run_pipeline
        st.info("Pipeline will run here. Coming next.")

st.write(" ")
if st.button("← Back to Profile", use_container_width=False):
    st.switch_page("pages/2_profile.py")