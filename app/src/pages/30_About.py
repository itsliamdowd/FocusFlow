import streamlit as st
from modules.nav import SideBarLinks

st.set_page_config(layout='wide')

SideBarLinks()

st.write("# About this App")

st.markdown(
    """
    FocusFlow is a data-driven productivity and focus management app built to help students,
    professors, and analysts manage time, track focus sessions, and gain insights into productivity.


    FocusFlow supports four user types:

    - Students: task and timer management
    - Professors: course and assignment oversight
    - Data analysts: productivity trend analysis
    - System administrators: data quality and platform monitoring
    """
)

# Add a button to return to home page
if st.button("Return to Home", type="primary"):
    st.switch_page("Home.py")
