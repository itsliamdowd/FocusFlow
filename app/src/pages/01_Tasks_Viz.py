import logging
logger = logging.getLogger(__name__)

import streamlit as st
import requests
from modules.nav import SideBarLinks

st.set_page_config(layout='wide')
SideBarLinks()

BASE_URL = 'http://api:4000/student'
user_id = st.session_state.get('user_id', 1)

st.title("Tasks")

# Load tasks from backend
tasks = []
load_error = None
try:
    response = requests.get(f"{BASE_URL}/tasks", params={"user_id": user_id})
    if response.status_code == 200:
        tasks = response.json().get('tasks', [])
    else:
        load_error = response.json().get('error', 'Unable to load tasks.')
except requests.exceptions.RequestException as exc:
    load_error = str(exc)

if load_error:
    st.warning(f"Tasks service unavailable: {load_error}")

# Add task
with st.form("add_task"):
    title = st.text_input("Task Title")
    category = st.selectbox("Category", ["School", "Work", "Extracurricular"])
    priority = st.selectbox("Priority", ["Low", "Medium", "High"])
    submitted = st.form_submit_button("Add Task")

    if submitted:
        if not title:
            st.error("Task title is required.")
        else:
            payload = {
                "user_id": user_id,
                "title": title,
                "category": category,
                "priority": priority,
                "time_allocated": 0
            }
            try:
                create_response = requests.post(f"{BASE_URL}/tasks", json=payload)
                if create_response.status_code == 201:
                    st.success("Task added!")
                    st.experimental_rerun()
                else:
                    st.error(create_response.json().get('error', 'Failed to create task.'))
            except requests.exceptions.RequestException as exc:
                st.error(f"Failed to connect to the task service: {exc}")

# Display tasks
st.subheader("Your Tasks")

if not tasks:
    st.info("No tasks have been added yet.")

for task in tasks:
    col1, col2 = st.columns([4,1])
    with col1:
        st.write(f"**{task.get('title', 'Untitled')}** ({task.get('category', 'Uncategorized')}, {task.get('priority', 'Medium')})")
    with col2:
        task_id = task.get('task_id')
        if task_id is None:
            continue
        delete_key = f"task_delete_{task_id}"
        if st.button("Delete", key=delete_key):
            try:
                delete_response = requests.delete(f"{BASE_URL}/tasks/{task_id}")
                if delete_response.status_code == 200:
                    st.success("Task deleted.")
                    st.experimental_rerun()
                else:
                    st.error(delete_response.json().get('error', 'Unable to delete task.'))
            except requests.exceptions.RequestException as exc:
                st.error(f"Could not reach task service: {exc}")
