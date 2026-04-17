import logging
logger = logging.getLogger(__name__)

import streamlit as st
import requests
from modules.nav import SideBarLinks

st.set_page_config(layout='wide')

# Show appropriate sidebar links for the role of the currently logged in user
SideBarLinks()

BASE_URL = 'http://api:4000/student'
user_id = st.session_state.get('user_id', 1)

st.session_state.setdefault('filter', 'All')

first_name = st.session_state.get('first_name', 'Student')

st.title(f"Welcome student, {first_name}.")
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

# Load tasks from backend
tasks = []
load_error = None
try:
    task_response = requests.get(f"{BASE_URL}/tasks", params={"user_id": user_id})
    if task_response.status_code == 200:
        tasks = task_response.json().get('tasks', [])
    else:
        load_error = task_response.json().get('error', 'Unable to load tasks from the backend.')
except requests.exceptions.RequestException as exc:
    load_error = str(exc)

if load_error:
    st.warning(f"Tasks service unavailable: {load_error}")

# Layout
left, right = st.columns(2)

with left:
    st.subheader("Tasks")

    filtered_tasks = tasks
    if st.session_state['filter'] != 'All':
        filtered_tasks = [task for task in tasks if task.get('category') == st.session_state['filter']]

    if len(filtered_tasks) == 0:
        st.info("No tasks to show for the selected filter.")
    for idx, task in enumerate(filtered_tasks):
        st.write(f"**{task.get('title', 'Untitled')}** ({task.get('category', 'Unknown')}, {task.get('priority', 'Medium')})")
        st.button("Start", key=f"start_{idx}_{task.get('title', idx)}")

with right:
    st.subheader("Calendar")
    st.date_input("Select Date")
