"""
Enter your name → new or returning user.
"""

import streamlit as st
import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from user.db.db_queries import get_user_by_name, create_user

st.set_page_config(page_title="Login", layout="centered")

st.title("Resume Platform")
st.write("---")

name = st.text_input("Enter your name to get started").strip()

if st.button("Continue", use_container_width=True):
    if not name:
        st.warning("Please enter your name.")
    else:
        user = get_user_by_name(name)

        if user:
            # Returning user
            st.session_state["user_id"]   = user["id"]
            st.session_state["user_name"] = user["name"]
            st.session_state["is_new"]    = False
            st.switch_page("pages/2_profile.py")
        else:
            # New user — create record immediately
            user_id = create_user(name)

            # Create their folder
            user_folder = os.path.join("user", name.replace(" ", "_"))
            os.makedirs(os.path.join(user_folder, "uploads"),  exist_ok=True)
            os.makedirs(os.path.join(user_folder, "outputs"),  exist_ok=True)

            st.session_state["user_id"]   = user_id
            st.session_state["user_name"] = name
            st.session_state["is_new"]    = True
            st.session_state["section"]   = 0   # start at first section
            st.switch_page("pages/2_profile.py")