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
        border: none;
        border-radius: 0;
        padding: 0.2rem 0.2rem 0.2rem 0.1rem;
        background: transparent;
        margin-bottom: 0.4rem;
        box-shadow: none;
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
    .task-meta {
        margin-bottom: 0.4rem;
    }
    .task-section-title {
        font-size: 1rem;
        font-weight: 700;
        color: #1e3a8a;
        margin: 0 0 0.45rem 0;
    }
    .task-section-help {
        color: #64748b;
        font-size: 0.86rem;
        margin: 0 0 0.7rem 0;
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
    div[data-testid="stForm"] {
        border: 1px solid #bfdbfe;
        border-radius: 14px;
        padding: 1rem 1rem 0.7rem 1rem;
        background: linear-gradient(180deg, #f8fbff, #eef4ff);
        box-shadow: 0 6px 14px rgba(30, 64, 175, 0.08);
        margin-bottom: 1rem;
    }
    .task-form-title {
        font-size: 1rem;
        font-weight: 700;
        color: #1e3a8a;
        margin-bottom: 0.2rem;
    }
    .task-form-help {
        margin: 0 0 0.55rem 0;
        color: #475569;
        font-size: 0.88rem;
    }
    div[data-testid="stForm"] label {
        font-weight: 600;
    }
    div[data-testid="stForm"] [data-baseweb="select"] {
        margin-bottom: 0.15rem;
    }
    div[data-testid="stForm"] .stFormSubmitButton > button {
        background: #2563eb;
        color: #ffffff;
        border: 1px solid #1d4ed8;
        border-radius: 10px;
        font-weight: 700;
    }
    div[data-testid="stForm"] .stFormSubmitButton > button:hover {
        background: #1d4ed8;
        border-color: #1e40af;
        color: #ffffff;
    }
    .stButton > button {
        background: #dc2626;
        color: #ffffff;
        border: 1px solid #b91c1c;
        border-radius: 10px;
        font-weight: 600;
        width: 100%;
        min-height: 2.3rem;
    }
    .stButton > button:hover {
        background: #b91c1c;
        border-color: #991b1b;
        color: #ffffff;
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

category_counts = {
    "school": 0,
    "work": 0,
    "extracurricular": 0,
    "personal": 0,
}
for task in tasks:
    category_name = (task.get("category") or "").strip().lower()
    if category_name in category_counts:
        category_counts[category_name] += 1

metric1, metric2, metric3, metric4, metric5 = st.columns(5)
metric1.metric("Total", len(tasks))
metric2.metric("School", category_counts["school"])
metric3.metric("Work", category_counts["work"])
metric4.metric("Extracurricular", category_counts["extracurricular"])
metric5.metric("Personal", category_counts["personal"])

entry_col, list_col = st.columns([2, 3], gap="large")

with entry_col:
    st.markdown('<div class="task-section-title">Add a New Task</div>', unsafe_allow_html=True)
    st.markdown('<p class="task-section-help">Create a task on the left, then manage your list on the right.</p>', unsafe_allow_html=True)

    with st.form("add_task", clear_on_submit=True):
        st.markdown('<div class="task-form-title">Quick Task Entry</div>', unsafe_allow_html=True)
        st.markdown(
            '<p class="task-form-help">Add a short task, choose category and priority, then save.</p>',
            unsafe_allow_html=True
        )

        title = st.text_input(
            "Task Title",
            placeholder="e.g., Review chapter 6 notes",
            help="Use a short, action-based title."
        )
        category = st.selectbox(
            "Category",
            ["school", "work", "extracurricular", "personal"],
            index=0,
            help="Where this task fits in your day."
        )
        priority = st.selectbox(
            "Priority",
            ["low", "medium", "high"],
            index=1,
            help="Medium is a good default for most tasks."
        )
        submitted = st.form_submit_button("Add Task", use_container_width=True, type="primary")

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

with list_col:
    st.markdown('<div class="task-section-title">Your Tasks</div>', unsafe_allow_html=True)
    st.markdown('<p class="task-section-help">Delete finished or duplicate items to keep your queue focused.</p>', unsafe_allow_html=True)

    if not tasks:
        st.info("No tasks have been added yet.")

    for task in tasks:
        task_title = task.get('title', 'Untitled')
        category = task.get('category', 'uncategorized')
        priority = task.get('priority', 'medium').lower()
        task_id = task.get('task_id')

        with st.container(border=True):
            col1, col2 = st.columns([5, 1], vertical_alignment="center")

            with col1:
                st.markdown(
                    f"""
                    <div class="task-card">
                      <div class="task-title">{task_title}</div>
                      <div class="task-meta">
                        <span class="task-pill pill-category">{category}</span>
                        <span class="task-pill pill-priority-{priority}">{priority}</span>
                      </div>
                    </div>
                    """,
                    unsafe_allow_html=True
                )

            with col2:
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