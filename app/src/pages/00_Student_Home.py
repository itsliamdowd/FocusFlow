import logging
logger = logging.getLogger(__name__)

import streamlit as st
from modules.nav import SideBarLinks

st.set_page_config(layout='wide')

# Show appropriate sidebar links for the role of the currently logged in user
SideBarLinks()

st.title(f"Welcome student, {st.session_state['first_name']}.")
st.write('### What would you like to do today?')

# Filters
col1, col2, col3, col4 = st.columns(4)

if col1.button("All Tasks"):
    st.session_state.filter = "All"
if col2.button("School"):
    st.session_state.filter = "School"
if col3.button("Work"):
    st.session_state.filter = "Work"
if col4.button("Extracurricular"):
    st.session_state.filter = "Extracurricular"

# Layout
left, right = st.columns(2)

with left:
    st.subheader("Tasks")

    for task in st.session_state.tasks:
        st.write(f"**{task['title']}** ({task['priority']})")
        st.button("Start", key=task["title"])

with right:
    st.subheader("Calendar")
    st.date_input("Select Date")
