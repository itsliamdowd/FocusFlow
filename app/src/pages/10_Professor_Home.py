import logging
logger = logging.getLogger(__name__)

import streamlit as st
from modules.nav import SideBarLinks

st.set_page_config(layout='wide')

SideBarLinks()

st.title(f"Welcome, {st.session_state['first_name']}.")
st.write('### What would you like to do today?')

if st.button('Manage My Courses', type='primary', use_container_width=True):
    st.switch_page('pages/11_Professor_Courses.py')

if st.button('View Student Roster', type='primary', use_container_width=True):
    st.switch_page('pages/12_Professor_Roster.py')

if st.button('Manage Assignments', type='primary', use_container_width=True):
    st.switch_page('pages/13_Professor_Assignments.py')
