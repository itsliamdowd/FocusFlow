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

st.markdown(
    """
    <style>
        .student-hero {
            border-radius: 16px;
            padding: 1.2rem 1.4rem;
            background: radial-gradient(circle at top right, #3b82f6 0%, #2563eb 45%, #1d4ed8 100%);
            color: #eff6ff;
            border: 1px solid rgba(191, 219, 254, 0.35);
            box-shadow: 0 14px 28px rgba(30, 64, 175, 0.28);
            margin-bottom: 1rem;
        }
        .student-hero h1 {
            margin: 0;
            font-size: 1.85rem;
        }
        .student-hero p {
            margin: 0.4rem 0 0 0;
            color: #dbeafe;
        }
        .section-title {
            color: #1e3a8a;
            font-size: 1rem;
            font-weight: 700;
            margin-top: 0.2rem;
            margin-bottom: 0.6rem;
            letter-spacing: 0.01em;
        }
        .task-row {
            padding: 0.75rem 0.3rem 0.2rem 0.3rem;
        }
        .task-title {
            font-weight: 700;
            color: #0f172a;
            margin-bottom: 0.35rem;
        }
        .task-meta {
            color: #475569;
            font-size: 0.86rem;
        }
        .category-pill {
            display: inline-block;
            border-radius: 999px;
            padding: 0.18rem 0.56rem;
            border: 1px solid #93c5fd;
            background: #dbeafe;
            color: #1e3a8a;
            font-size: 0.76rem;
            font-weight: 600;
            margin-right: 0.35rem;
        }
        .priority-low {
            border-color: #86efac;
            background: #dcfce7;
            color: #166534;
        }
        .priority-medium {
            border-color: #fcd34d;
            background: #fef3c7;
            color: #92400e;
        }
        .priority-high {
            border-color: #fca5a5;
            background: #fee2e2;
            color: #991b1b;
        }
        .calendar-help {
            color: #475569;
            font-size: 0.9rem;
            margin-bottom: 0.45rem;
        }
        .stButton > button {
            border-radius: 10px;
            font-weight: 600;
            white-space: nowrap;
            min-height: 2.35rem;
        }
    </style>
    """,
    unsafe_allow_html=True,
)

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

category_counts = {
    "school": 0,
    "work": 0,
    "extracurricular": 0,
    "personal": 0,
}
for task in tasks:
    category = (task.get("category") or "").strip().lower()
    if category in category_counts:
        category_counts[category] += 1

st.markdown(
    f"""
    <div class="student-hero">
      <h1>Welcome back, {first_name}</h1>
      <p>Pick a task, launch focus mode, and keep your momentum moving today.</p>
    </div>
    """,
    unsafe_allow_html=True,
)

metric_1, metric_2, metric_3, metric_4 = st.columns(4)
metric_1.metric("Total Tasks", len(tasks))
metric_2.metric("School", category_counts["school"])
metric_3.metric("Work", category_counts["work"])
metric_4.metric("Extracurricular", category_counts["extracurricular"])

st.markdown('<div class="section-title">Filter Your Tasks</div>', unsafe_allow_html=True)
f1, f2, f3, f4, f5 = st.columns([1, 1, 1, 1.55, 1])
if f1.button("All", use_container_width=True):
    st.session_state.filter = "all"
if f2.button("School", use_container_width=True):
    st.session_state.filter = "school"
if f3.button("Work", use_container_width=True):
    st.session_state.filter = "work"
if f4.button("Extracurricular", use_container_width=True):
    st.session_state.filter = "extracurricular"
if f5.button("Personal", use_container_width=True):
    st.session_state.filter = "personal"

st.caption(f"Showing: **{st.session_state.filter.title()}**")

left, right = st.columns(2)

with left:
    st.markdown('<div class="section-title">Your Tasks</div>', unsafe_allow_html=True)

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
        category = (task.get("category", "unknown") or "unknown").lower()
        priority = (task.get("priority", "medium") or "medium").lower()
        safe_priority = priority if priority in {"low", "medium", "high"} else "medium"

        with st.container(border=True):
            details_col, action_col = st.columns([4.5, 1.5], vertical_alignment="center")
            with details_col:
                st.markdown(
                    f"""
                    <div class="task-row">
                      <div class="task-title">{title}</div>
                      <div class="task-meta">
                        <span class="category-pill">{category}</span>
                        <span class="category-pill priority-{safe_priority}">{safe_priority}</span>
                      </div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )
            with action_col:
                if st.button("Focus", key=f"start_{task_id or idx}"):
                    if task_id is not None:
                        st.session_state["selected_task_id"] = task_id
                        st.switch_page("pages/02_Timer.py")

with right:
    st.markdown('<div class="section-title">Plan Your Day</div>', unsafe_allow_html=True)
    st.markdown('<p class="calendar-help">Use this as a quick planning anchor, then jump into Focus mode on the left.</p>', unsafe_allow_html=True)
    selected_date = st.date_input("Select Date")
    st.info(f"Schedule snapshot for {selected_date.strftime('%B %d, %Y')} is ready.")

# Reliable page-end spacer so the dashboard never feels cramped at the bottom.
st.markdown("<div style='height: 140px;'></div>", unsafe_allow_html=True)