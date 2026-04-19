import logging
import time
from datetime import datetime

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
        .timer-hero {
            background: #1d4ed8;
            border: 1px solid #1e40af;
            border-radius: 16px;
            padding: 1.25rem 1.4rem;
            color: #eff6ff;
            margin-bottom: 1rem;
        }
        .timer-hero h1 {
            margin: 0;
            font-size: 1.8rem;
        }
        .timer-hero p {
            margin: 0.4rem 0 0 0;
            color: #dbeafe;
        }
        .timer-clock {
            text-align: center;
            font-size: 2.4rem;
            font-weight: 700;
            color: #0f172a;
            margin: 0.5rem 0 0.7rem;
            letter-spacing: 1.2px;
        }
        .timer-caption {
            color: #64748b;
            font-size: 0.9rem;
            text-align: center;
            margin: 0;
        }
        .stButton button {
            border-radius: 10px;
            font-weight: 600;
        }
    </style>
    """,
    unsafe_allow_html=True,
)

st.markdown(
    """
    <div class="timer-hero">
        <h1>Focus Timer</h1>
        <p>Stay on task with a simple Pomodoro workflow and automatic session tracking.</p>
    </div>
    """,
    unsafe_allow_html=True,
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

    return {
        "Content-Type": "application/json",
        "X-User-Role": role_map.get(role, role),
        "X-User-Id": str(user_id),
    }


def format_time(sec):
    return f"{sec // 60:02d}:{sec % 60:02d}"


# Timer state
if "time_left" not in st.session_state:
    st.session_state.time_left = 1800  # 30 minutes

if "running" not in st.session_state:
    st.session_state.running = False

if "active_session_id" not in st.session_state:
    st.session_state.active_session_id = None

if "selected_task_id" not in st.session_state:
    st.session_state.selected_task_id = None


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
        tasks = response.json().get("tasks", [])
    else:
        try:
            load_error = response.json().get("error", "Unable to load tasks.")
        except ValueError:
            load_error = "Unable to load tasks."
except requests.exceptions.RequestException as exc:
    load_error = str(exc)

if load_error:
    st.warning(f"Task service unavailable: {load_error}")


task_map = {task["task_id"]: task["title"] for task in tasks if "task_id" in task}
task_ids = list(task_map.keys())

selected_task_id = None
if task_ids:
    default_index = 0
    if st.session_state.selected_task_id in task_ids:
        default_index = task_ids.index(st.session_state.selected_task_id)

    selected_task_id = st.selectbox(
        "Choose Task",
        task_ids,
        index=default_index,
        format_func=lambda task_id: task_map.get(task_id, f"Task {task_id}")
    )
    st.session_state.selected_task_id = selected_task_id
else:
    st.info("Create a task first before starting a timer.")


st.subheader("Pomodoro Timer")
st.markdown(f'<div class="timer-clock">{format_time(st.session_state.time_left)}</div>', unsafe_allow_html=True)
st.markdown('<p class="timer-caption">MM:SS remaining in current focus block</p>', unsafe_allow_html=True)

primary_bg = "#dc2626" if st.session_state.running else "#16a34a"
primary_border = "#b91c1c" if st.session_state.running else "#15803d"
primary_hover = "#b91c1c" if st.session_state.running else "#15803d"
st.markdown(
    f"""
    <style>
        div[data-testid="stHorizontalBlock"] > div[data-testid="stColumn"]:first-child div.stButton > button {{
            background-color: {primary_bg};
            color: #ffffff;
            border: 1px solid {primary_border};
        }}
        div[data-testid="stHorizontalBlock"] > div[data-testid="stColumn"]:first-child div.stButton > button:hover {{
            background-color: {primary_hover};
            color: #ffffff;
            border: 1px solid {primary_border};
        }}
    </style>
    """,
    unsafe_allow_html=True,
)

col1, col2 = st.columns(2)

with col1:
    primary_label = "Stop" if st.session_state.running else "Start"
    if st.button(primary_label, disabled=selected_task_id is None):
        if not st.session_state.running and selected_task_id is not None:
            payload = {
                "user_id": user_id,
                "start_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "session_type": "pomodoro"
            }

            try:
                start_response = requests.post(
                    f"{BASE_URL}/tasks/{selected_task_id}/sessions",
                    json=payload,
                    headers=build_headers(),
                    timeout=10
                )
                if start_response.status_code in [200, 201]:
                    data = start_response.json()
                    st.session_state.active_session_id = data.get("session_id")
                    st.session_state.running = True
                    st.success("Timer started.")
                    st.rerun()
                else:
                    try:
                        st.error(start_response.json().get("error", "Unable to start timer session."))
                    except ValueError:
                        st.error("Unable to start timer session.")
            except requests.exceptions.RequestException as exc:
                st.error(f"Could not connect to timer service: {exc}")
        elif st.session_state.running:
            if selected_task_id is not None and st.session_state.active_session_id is not None:
                elapsed_seconds = max(0, 1800 - st.session_state.time_left)
                elapsed_minutes = max(1, (elapsed_seconds + 59) // 60)
                payload = {
                    "session_id": st.session_state.active_session_id,
                    "end_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "duration": elapsed_minutes
                }

                try:
                    stop_response = requests.put(
                        f"{BASE_URL}/tasks/{selected_task_id}/sessions",
                        json=payload,
                        headers=build_headers(),
                        timeout=10
                    )
                    if stop_response.status_code in [200, 201]:
                        st.success("Timer stopped. Session saved.")
                    else:
                        try:
                            st.error(stop_response.json().get("error", "Unable to save timer session."))
                        except ValueError:
                            st.error("Unable to save timer session.")
                except requests.exceptions.RequestException as exc:
                    st.error(f"Could not connect to timer service: {exc}")

            st.session_state.running = False
            st.session_state.time_left = 1800
            st.session_state.active_session_id = None
            st.rerun()

with col2:
    if st.button("Reset"):
        st.session_state.running = False
        st.session_state.time_left = 1800
        st.session_state.active_session_id = None
        st.rerun()


# Timer loop
if st.session_state.running:
    time.sleep(1)
    st.session_state.time_left -= 1

    if st.session_state.time_left <= 0:
        if selected_task_id is not None and st.session_state.active_session_id is not None:
            payload = {
                "session_id": st.session_state.active_session_id,
                "end_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "duration": 30
            }

            try:
                end_response = requests.put(
                    f"{BASE_URL}/tasks/{selected_task_id}/sessions",
                    json=payload,
                    headers=build_headers(),
                    timeout=10
                )
                if end_response.status_code in [200, 201]:
                    st.success("Pomodoro complete. Session saved.")
                else:
                    try:
                        st.error(end_response.json().get("error", "Unable to save timer session."))
                    except ValueError:
                        st.error("Unable to save timer session.")
            except requests.exceptions.RequestException as exc:
                st.error(f"Could not connect to timer service: {exc}")

        st.session_state.running = False
        st.session_state.time_left = 1800
        st.session_state.active_session_id = None

    st.rerun()


st.subheader("Saved Sessions")

if selected_task_id is not None:
    try:
        session_response = requests.get(
            f"{BASE_URL}/tasks/{selected_task_id}/sessions",
            headers=build_headers(),
            timeout=10
        )
        if session_response.status_code == 200:
            session_data = session_response.json()
            sessions = session_data.get("sessions", [])
            total_time = session_data.get("total_time", 0)

            st.write(f"Total Time Logged: {total_time} minutes")

            if sessions:
                st.dataframe(sessions, use_container_width=True)
            else:
                st.info("No sessions found for this task yet.")
        else:
            try:
                st.warning(session_response.json().get("error", "Unable to load sessions."))
            except ValueError:
                st.warning("Unable to load sessions.")
    except requests.exceptions.RequestException as exc:
        st.warning(f"Session service unavailable: {exc}")