import logging
import time
import math
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
            white-space: nowrap;
            line-height: 1;
            min-width: 8.5rem;
            padding-left: 0.75rem;
            padding-right: 0.75rem;
        }
        .timeline-wrap {
            border: 1px solid #dbeafe;
            border-radius: 14px;
            padding: 0.75rem;
            background: #ffffff;
            box-shadow: 0 8px 16px rgba(30, 64, 175, 0.08);
            margin-bottom: 0.75rem;
        }
        .timeline-row {
            display: flex;
            flex-wrap: wrap;
            gap: 0.45rem;
        }
        .timeline-chip {
            border-radius: 999px;
            padding: 0.34rem 0.62rem;
            font-size: 0.78rem;
            font-weight: 700;
            border: 1px solid #bfdbfe;
            background: #eff6ff;
            color: #1e3a8a;
        }
        .timeline-done {
            background: #dcfce7;
            border-color: #86efac;
            color: #166534;
        }
        .timeline-current {
            background: #fef3c7;
            border-color: #fcd34d;
            color: #92400e;
        }
        .timeline-upcoming {
            background: #f8fafc;
            border-color: #e2e8f0;
            color: #64748b;
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

if "active_task_id" not in st.session_state:
    st.session_state.active_task_id = None

if "selected_task_id" not in st.session_state:
    st.session_state.selected_task_id = None

if "timeline_task_id" not in st.session_state:
    st.session_state.timeline_task_id = None

if "break_alert_marks" not in st.session_state:
    st.session_state.break_alert_marks = {}

if "current_required_minutes" not in st.session_state:
    st.session_state.current_required_minutes = 30


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
task_details = {task["task_id"]: task for task in tasks if "task_id" in task}
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

# Determine required assignment time and already logged time.
required_minutes = 30
completed_minutes = 0
remaining_minutes = 30
if selected_task_id is not None:
    selected_task = task_details.get(selected_task_id, {})
    try:
        required_minutes = int(selected_task.get("time_allocated") or 0)
    except (TypeError, ValueError):
        required_minutes = 0
    if required_minutes <= 0:
        required_minutes = 30

    try:
        totals_response = requests.get(
            f"{BASE_URL}/tasks/{selected_task_id}/sessions",
            headers=build_headers(),
            timeout=10
        )
        if totals_response.status_code == 200:
            completed_minutes = max(0, int(float(totals_response.json().get("total_time", 0) or 0)))
    except (requests.exceptions.RequestException, ValueError, TypeError):
        completed_minutes = 0

    completed_minutes = min(completed_minutes, required_minutes)
    remaining_minutes = max(required_minutes - completed_minutes, 0)
    st.session_state.current_required_minutes = required_minutes

    # Keep timer in sync with task remaining time when no active session is running.
    if st.session_state.active_session_id is None and st.session_state.timeline_task_id != selected_task_id:
        st.session_state.time_left = remaining_minutes * 60
        st.session_state.timeline_task_id = selected_task_id


st.subheader("Pomodoro Timer")
st.markdown(f'<div class="timer-clock">{format_time(st.session_state.time_left)}</div>', unsafe_allow_html=True)
required_seconds = max(60, int(st.session_state.current_required_minutes * 60))
session_progress = min(1.0, max(0.0, (required_seconds - st.session_state.time_left) / required_seconds))
st.progress(session_progress)
st.markdown('<p class="timer-caption">MM:SS remaining in current focus block</p>', unsafe_allow_html=True)
st.caption(
    f"Planned: {required_minutes} min • Logged: {completed_minutes} min • Remaining: {max(0, math.ceil(st.session_state.time_left / 60))} min"
)

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
        div[data-testid="stHorizontalBlock"] > div[data-testid="stColumn"]:nth-child(2) div.stButton > button {{
            background-color: #dc2626;
            color: #ffffff;
            border: 1px solid #b91c1c;
        }}
        div[data-testid="stHorizontalBlock"] > div[data-testid="stColumn"]:nth-child(2) div.stButton > button:hover {{
            background-color: #b91c1c;
            color: #ffffff;
            border: 1px solid #991b1b;
        }}
    </style>
    """,
    unsafe_allow_html=True,
)

col1, col2 = st.columns(2, gap="small")

with col1:
    if st.session_state.active_session_id is None:
        primary_label = "▶ Play"
        primary_disabled = selected_task_id is None
    elif st.session_state.running:
        primary_label = "⏸ Pause"
        primary_disabled = False
    else:
        primary_label = "▶ Play"
        primary_disabled = False

    if st.button(primary_label, disabled=primary_disabled, use_container_width=True):
        if st.session_state.active_session_id is None and selected_task_id is not None:
            if st.session_state.time_left <= 0:
                st.info("This task's planned time is complete. Press Stop to reset or choose another task.")
                st.stop()
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
                    st.session_state.active_task_id = selected_task_id
                    st.session_state.running = True
                    st.rerun()
                else:
                    try:
                        st.error(start_response.json().get("error", "Unable to start timer session."))
                    except ValueError:
                        st.error("Unable to start timer session.")
            except requests.exceptions.RequestException as exc:
                st.error(f"Could not connect to timer service: {exc}")
        elif st.session_state.running:
            # Pause keeps the current session active so user can resume later.
            st.session_state.running = False
            st.rerun()
        elif st.session_state.active_session_id is not None:
            # Resume previously paused active session.
            st.session_state.running = True
            st.rerun()

with col2:
    if st.button("⏹ Stop", disabled=st.session_state.active_session_id is None, use_container_width=True):
        active_task_id = st.session_state.active_task_id
        if active_task_id is not None:
            payload = {
                "session_id": st.session_state.active_session_id,
                "end_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "duration": 0
            }
            try:
                stop_response = requests.put(
                    f"{BASE_URL}/tasks/{active_task_id}/sessions",
                    json=payload,
                    headers=build_headers(),
                    timeout=10
                )
                if stop_response.status_code not in [200, 201]:
                    try:
                        st.error(stop_response.json().get("error", "Unable to stop timer session."))
                    except ValueError:
                        st.error("Unable to stop timer session.")
            except requests.exceptions.RequestException as exc:
                st.error(f"Could not connect to timer service: {exc}")

        st.session_state.running = False
        st.session_state.time_left = remaining_minutes * 60
        st.session_state.active_session_id = None
        st.session_state.active_task_id = None
        st.rerun()


# Timer loop
if st.session_state.running:
    prev_time_left = st.session_state.time_left
    time.sleep(1)
    st.session_state.time_left -= 1

    task_alert_key = str(st.session_state.active_task_id or selected_task_id or "none")
    shown_marks = set(st.session_state.break_alert_marks.get(task_alert_key, []))
    prev_completed = max(0, required_seconds - prev_time_left)
    current_completed = max(0, required_seconds - st.session_state.time_left)
    for mark in range(20 * 60, required_seconds + 1, 20 * 60):
        if prev_completed < mark <= current_completed and mark not in shown_marks:
            msg = f"Break reminder: you've focused for {mark // 60} minutes. Take 5 minutes."
            if hasattr(st, "toast"):
                st.toast(msg)
            else:
                st.info(msg)
            shown_marks.add(mark)
    st.session_state.break_alert_marks[task_alert_key] = sorted(shown_marks)

    if st.session_state.time_left <= 0:
        active_task_id = st.session_state.active_task_id
        if active_task_id is not None and st.session_state.active_session_id is not None:
            elapsed_seconds = max(0, required_seconds - st.session_state.time_left)
            elapsed_minutes = max(1, (elapsed_seconds + 59) // 60)
            payload = {
                "session_id": st.session_state.active_session_id,
                "end_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "duration": elapsed_minutes
            }

            try:
                end_response = requests.put(
                    f"{BASE_URL}/tasks/{active_task_id}/sessions",
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
        st.session_state.time_left = 0
        st.session_state.active_session_id = None
        st.session_state.active_task_id = None

    st.rerun()


st.subheader("Timeline")
timeline_required = max(1, int(st.session_state.current_required_minutes))
timeline_completed = max(0, timeline_required - math.ceil(max(0, st.session_state.time_left) / 60))
timeline_rows = []
focus_completed = 0
focus_block_num = 1
while focus_completed < timeline_required:
    focus_duration = min(20, timeline_required - focus_completed)
    focus_end = focus_completed + focus_duration
    timeline_rows.append(
        {
            "segment": f"Focus {focus_block_num}",
            "duration_min": focus_duration,
            "status": "Done" if timeline_completed >= focus_end else "Pending",
        }
    )
    focus_completed = focus_end

    if focus_completed < timeline_required:
        timeline_rows.append(
            {
                "segment": f"Break {focus_block_num}",
                "duration_min": 5,
                "status": "Done" if timeline_completed >= focus_completed else "Pending",
            }
        )
    focus_block_num += 1

# Exactly one active segment at a time.
current_index = None
for idx, row in enumerate(timeline_rows):
    if row["status"] != "Done":
        current_index = idx
        break

chip_html = []
for idx, row in enumerate(timeline_rows):
    if row["status"] == "Done":
        status_class = "timeline-done"
        status_label = "Done"
    elif idx == current_index:
        status_class = "timeline-current"
        status_label = "Current"
    else:
        status_class = "timeline-upcoming"
        status_label = ""
    label = (
        f"{row['segment']} • {row['duration_min']}m • {status_label}"
        if status_label
        else f"{row['segment']} • {row['duration_min']}m"
    )
    chip_html.append(f'<span class="timeline-chip {status_class}">{label}</span>')

# Extra final milestone badge (separate from the current segment highlight).
finish_class = "timeline-done" if timeline_completed >= timeline_required else "timeline-upcoming"
finish_label = "🏁 Finished" if timeline_completed >= timeline_required else "🏁 Finish"
chip_html.append(f'<span class="timeline-chip {finish_class}">{finish_label}</span>')

st.markdown(
    f"""
    <div class="timeline-wrap">
      <div class="timeline-row">
        {''.join(chip_html)}
      </div>
    </div>
    """,
    unsafe_allow_html=True,
)


st.subheader("Saved Sessions")

if selected_task_id is not None:
    if st.session_state.running:
        st.caption("Session history refreshes when paused or stopped.")
    else:
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