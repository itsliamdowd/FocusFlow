import logging
import requests
import streamlit as st
from modules.nav import SideBarLinks

logger = logging.getLogger(__name__)

st.set_page_config(layout='wide')
SideBarLinks()

BASE_URL = 'http://api:4000/student'
user_id = st.session_state.get('user_id', 25)
role = st.session_state.get('role', 'student')

st.title("Tasks")


def build_headers():
    role_map = {
        "student": "student",
        "professor": "professor",
        "data analyst": "analyst",
        "system admin": "admin",
        "analyst": "analyst",
        "admin": "admin",
    }

    headers = {
        "Content-Type": "application/json",
        "X-User-Role": role_map.get(role, role),
        "X-User-Id": str(user_id),
    }

    return headers


# Load tasks from backend
tasks = []
load_error = None
try:
    response = requests.get(
        f"{BASE_URL}/tasks",
        params={"user_id": user_id},
        headers=build_headers(),
        timeout=10
    )
    if response.status_code == 200:
        tasks = response.json().get('tasks', [])
    else:
        try:
            load_error = response.json().get('error', 'Unable to load tasks.')
        except ValueError:
            load_error = 'Unable to load tasks.'
except requests.exceptions.RequestException as exc:
    load_error = str(exc)

if load_error:
    st.warning(f"Tasks service unavailable: {load_error}")


# Add task
with st.form("add_task"):
    title = st.text_input("Task Title")
    category = st.selectbox("Category", ["school", "work", "extracurricular", "personal"])
    priority = st.selectbox("Priority", ["low", "medium", "high"])
    submitted = st.form_submit_button("Add Task")

    if submitted:
        if not title.strip():
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
                create_response = requests.post(
                    f"{BASE_URL}/tasks",
                    json=payload,
                    headers=build_headers(),
                    timeout=10
                )
                if create_response.status_code in [200, 201]:
                    st.success("Task added!")
                    st.rerun()
                else:
                    try:
                        st.error(create_response.json().get('error', 'Failed to create task.'))
                    except ValueError:
                        st.error('Failed to create task.')
            except requests.exceptions.RequestException as exc:
                st.error(f"Failed to connect to the task service: {exc}")


# Display tasks
st.subheader("Your Tasks")

if not tasks:
    st.info("No tasks have been added yet.")

for task in tasks:
    col1, col2 = st.columns([4, 1])

    with col1:
        st.write(
            f"**{task.get('title', 'Untitled')}** "
            f"({task.get('category', 'uncategorized')}, "
            f"{task.get('priority', 'medium')})"
        )

    with col2:
        task_id = task.get('task_id')
        if task_id is None:
            continue

        delete_key = f"task_delete_{task_id}"
        if st.button("Delete", key=delete_key):
            try:
                delete_response = requests.delete(
                    f"{BASE_URL}/tasks/{task_id}",
                    headers=build_headers(),
                    timeout=10
                )
                if delete_response.status_code == 200:
                    st.success("Task deleted.")
                    st.rerun()
                else:
                    try:
                        st.error(delete_response.json().get('error', 'Unable to delete task.'))
                    except ValueError:
                        st.error('Unable to delete task.')
            except requests.exceptions.RequestException as exc:
                st.error(f"Could not reach task service: {exc}")