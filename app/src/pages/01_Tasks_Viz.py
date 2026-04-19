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

st.markdown(
    """
    <style>
    .task-hero {
        border-radius: 16px;
        padding: 1.25rem 1.5rem;
        background: #1e40af;
        color: #f9fafb;
        margin-bottom: 1rem;
        box-shadow: 0 10px 20px rgba(30, 64, 175, 0.35);
    }
    .task-hero h1 {
        margin: 0;
        font-size: 2rem;
    }
    .task-hero p {
        margin: 0.35rem 0 0 0;
        color: #dbeafe;
    }
    .task-card {
        border: 1px solid rgba(15, 23, 42, 0.16);
        border-radius: 14px;
        padding: 0.85rem 1rem;
        background: rgba(255, 255, 255, 0.96);
        margin-bottom: 0.65rem;
        box-shadow: 0 6px 16px rgba(2, 6, 23, 0.1);
    }
    .task-title {
        font-weight: 700;
        color: #0f172a;
        margin-bottom: 0.45rem;
        line-height: 1.3;
    }
    .task-pill {
        display: inline-block;
        border-radius: 999px;
        padding: 0.15rem 0.55rem;
        margin-right: 0.45rem;
        font-size: 0.78rem;
        font-weight: 600;
        letter-spacing: 0.01em;
    }
    .pill-category {
        background: #dbeafe;
        color: #1e3a8a;
        border: 1px solid #93c5fd;
    }
    .pill-priority-low {
        background: #dcfce7;
        color: #166534;
        border: 1px solid #86efac;
    }
    .pill-priority-medium {
        background: #fef3c7;
        color: #92400e;
        border: 1px solid #fcd34d;
    }
    .pill-priority-high {
        background: #fee2e2;
        color: #991b1b;
        border: 1px solid #fca5a5;
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.markdown(
    """
    <div class="task-hero">
      <h1>Task Studio</h1>
      <p>Organize what matters and keep your momentum.</p>
    </div>
    """,
    unsafe_allow_html=True
)


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
st.subheader("Add a New Task")
with st.form("add_task", clear_on_submit=True):
    left_col, right_col = st.columns([3, 2])
    with left_col:
        title = st.text_input("Task Title", placeholder="e.g., Review chapter notes")
    with right_col:
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
    task_title = task.get('title', 'Untitled')
    category = task.get('category', 'uncategorized')
    priority = task.get('priority', 'medium').lower()

    with col1:
        st.markdown(
            f"""
            <div class="task-card">
              <div class="task-title">{task_title}</div>
              <span class="task-pill pill-category">{category}</span>
              <span class="task-pill pill-priority-{priority}">{priority}</span>
            </div>
            """,
            unsafe_allow_html=True
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