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
first_name = st.session_state.get('first_name', 'Student')

st.session_state.setdefault('filter', 'all')


def build_headers():
    role_map = {
        "student": "student",
        "professor": "professor",
        "data analyst": "analyst",
        "system admin": "admin",
        "analyst": "analyst",
        "admin": "admin",
    }

    return {
        "Content-Type": "application/json",
        "X-User-Role": role_map.get(role, role),
        "X-User-Id": str(user_id),
    }


st.title(f"Welcome student, {first_name}.")
st.write("### What would you like to do today?")

# Filters
col1, col2, col3, col4 = st.columns(4)

if col1.button("All Tasks"):
    st.session_state.filter = "all"
if col2.button("School"):
    st.session_state.filter = "school"
if col3.button("Work"):
    st.session_state.filter = "work"
if col4.button("Extracurricular"):
    st.session_state.filter = "extracurricular"

# Load tasks from backend
tasks = []
load_error = None
try:
    task_response = requests.get(
        f"{BASE_URL}/tasks",
        params={"user_id": user_id},
        headers=build_headers(),
        timeout=10
    )
    if task_response.status_code == 200:
        tasks = task_response.json().get("tasks", [])
    else:
        try:
            load_error = task_response.json().get(
                "error",
                "Unable to load tasks from the backend."
            )
        except ValueError:
            load_error = "Unable to load tasks from the backend."
except requests.exceptions.RequestException as exc:
    load_error = str(exc)

if load_error:
    st.warning(f"Tasks service unavailable: {load_error}")

left, right = st.columns(2)

with left:
    st.subheader("Tasks")

    filtered_tasks = tasks
    if st.session_state["filter"] != "all":
        filtered_tasks = [
            task for task in tasks
            if task.get("category") == st.session_state["filter"]
        ]

    if len(filtered_tasks) == 0:
        st.info("No tasks to show for the selected filter.")

    for idx, task in enumerate(filtered_tasks):
        task_id = task.get("task_id")
        title = task.get("title", "Untitled")
        category = task.get("category", "unknown")
        priority = task.get("priority", "medium")

        st.write(f"**{title}** ({category}, {priority})")

        if st.button("Start", key=f"start_{task_id or idx}"):
            if task_id is not None:
                st.session_state["selected_task_id"] = task_id
                st.switch_page("pages/02_Timer.py")

with right:
    st.subheader("Calendar")
    st.date_input("Select Date")