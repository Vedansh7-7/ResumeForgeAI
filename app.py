import streamlit as st

st.set_page_config(page_title="Resume Platform", layout="centered")

# Redirect to login if no user in session
if "user_id" not in st.session_state:
    st.switch_page("pages/1_login.py")
else:
    st.switch_page("pages/2_profile.py")