import logging
import calendar
from datetime import date

import pandas as pd
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
            padding-bottom: 0.4rem;
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
        .focus-calendar-wrap {
            border: 1px solid #bfdbfe;
            border-radius: 14px;
            overflow: hidden;
            background: #ffffff;
            box-shadow: 0 8px 18px rgba(30, 64, 175, 0.08);
        }
        .focus-calendar-month {
            background: #1d4ed8;
            color: #eff6ff;
            font-weight: 700;
            padding: 0.55rem 0.75rem;
            font-size: 0.95rem;
            letter-spacing: 0.01em;
        }
        .focus-calendar-table {
            width: 100%;
            border-collapse: collapse;
            table-layout: fixed;
        }
        .focus-calendar-table th {
            background: #2563eb;
            color: #eff6ff;
            font-size: 0.8rem;
            font-weight: 700;
            padding: 0.45rem 0.3rem;
            border: 1px solid #1e40af;
            text-align: center;
        }
        .focus-calendar-table td {
            border: 1px solid #dbeafe;
            vertical-align: top;
            height: 62px;
            padding: 0.35rem 0.38rem;
            background: #ffffff;
        }
        .focus-calendar-empty {
            background: #f8fafc !important;
        }
        .focus-calendar-day {
            color: #0f172a;
            font-weight: 700;
            font-size: 0.84rem;
            line-height: 1.1;
        }
        .focus-calendar-minutes {
            margin-top: 0.2rem;
            color: #64748b;
            font-size: 0.76rem;
            line-height: 1.15;
        }
        .focus-calendar-active .focus-calendar-minutes {
            color: #1d4ed8;
            font-weight: 600;
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
    st.markdown('<div class="section-title">Daily Focus Calendar</div>', unsafe_allow_html=True)
    st.markdown(
        '<p class="calendar-help">Pick a date to see your logged focus minutes and a monthly calendar overview.</p>',
        unsafe_allow_html=True
    )

    activity_rows = []
    activity_error = None
    try:
        activity_response = requests.get(
            f"{BASE_URL}/activity",
            params={"user_id": user_id},
            headers=build_headers(),
            timeout=10
        )
        if activity_response.status_code == 200:
            activity_rows = activity_response.json().get("activity", [])
        else:
            try:
                activity_error = activity_response.json().get("error", "Unable to load focus activity.")
            except ValueError:
                activity_error = "Unable to load focus activity."
    except requests.exceptions.RequestException as exc:
        activity_error = str(exc)

    if activity_error:
        st.warning(f"Focus activity unavailable: {activity_error}")
    elif not activity_rows:
        st.info("No focus logs yet. Start a timer session to populate your calendar.")
    else:
        activity_df = pd.DataFrame(activity_rows)
        activity_df["log_date"] = pd.to_datetime(activity_df["log_date"], errors="coerce").dt.date
        activity_df["total_duration"] = pd.to_numeric(
            activity_df["total_duration"], errors="coerce"
        ).fillna(0).astype(int)
        activity_df = activity_df.dropna(subset=["log_date"])

        daily_totals = (
            activity_df.groupby("log_date", as_index=False)["total_duration"]
            .sum()
            .rename(columns={"total_duration": "focus_minutes"})
        )

        min_log_date = min(daily_totals["log_date"])
        max_log_date = max(daily_totals["log_date"])
        default_date = date.today()
        if default_date < min_log_date:
            default_date = min_log_date
        elif default_date > max_log_date:
            default_date = max_log_date

        selected_date = st.date_input(
            "Select Date",
            value=default_date,
            min_value=min_log_date,
            max_value=max_log_date,
        )

        selected_total = int(
            daily_totals.loc[daily_totals["log_date"] == selected_date, "focus_minutes"].sum()
        )
        st.metric("Focus Minutes on Selected Day", selected_total)

        selected_breakdown = (
            activity_df[activity_df["log_date"] == selected_date]
            .groupby("category", as_index=False)["total_duration"]
            .sum()
            .rename(columns={"total_duration": "minutes"})
            .sort_values("minutes", ascending=False)
        )
        if selected_breakdown.empty:
            st.caption(f"No logged focus activity for {selected_date.strftime('%B %d, %Y')}.")
        else:
            st.dataframe(selected_breakdown, hide_index=True, use_container_width=True)

        month_start = selected_date.replace(day=1)
        days_in_month = calendar.monthrange(selected_date.year, selected_date.month)[1]
        month_days = [month_start.replace(day=day) for day in range(1, days_in_month + 1)]
        month_df = pd.DataFrame({"date": month_days})
        month_df["day"] = month_df["date"].apply(lambda d: d.day)
        month_df["weekday"] = month_df["date"].apply(lambda d: d.weekday())  # Monday=0
        month_df["week"] = ((month_df["day"] + month_df.iloc[0]["weekday"] - 1) // 7) + 1

        totals_map = dict(zip(daily_totals["log_date"], daily_totals["focus_minutes"]))
        month_df["minutes"] = month_df["date"].map(totals_map).fillna(0).astype(int)
        day_lookup = {row["date"]: int(row["minutes"]) for _, row in month_df.iterrows()}
        first_weekday = month_start.weekday()  # Monday=0
        total_slots = first_weekday + days_in_month
        week_count = (total_slots + 6) // 7

        weekday_headers = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
        table_rows = []
        day_cursor = 1
        for week_idx in range(week_count):
            row_cells = []
            for weekday in range(7):
                slot_index = week_idx * 7 + weekday
                if slot_index < first_weekday or day_cursor > days_in_month:
                    row_cells.append('<td class="focus-calendar-empty"></td>')
                else:
                    current_date = month_start.replace(day=day_cursor)
                    minutes = day_lookup.get(current_date, 0)
                    active_class = " focus-calendar-active" if minutes > 0 else ""
                    minutes_label = f"{minutes} min" if minutes > 0 else ""
                    row_cells.append(
                        f'<td class="{active_class.strip()}"><div class="focus-calendar-day">{day_cursor}</div>'
                        f'<div class="focus-calendar-minutes">{minutes_label}</div></td>'
                    )
                    day_cursor += 1
            table_rows.append(f"<tr>{''.join(row_cells)}</tr>")

        header_html = "".join([f"<th>{d}</th>" for d in weekday_headers])
        calendar_html = (
            f'<div class="focus-calendar-wrap">'
            f'<div class="focus-calendar-month">{selected_date.strftime("%B %Y")}</div>'
            f'<table class="focus-calendar-table"><thead><tr>{header_html}</tr></thead>'
            f'<tbody>{"".join(table_rows)}</tbody></table></div>'
        )
        st.markdown(calendar_html, unsafe_allow_html=True)

# Reliable page-end spacer so the dashboard never feels cramped at the bottom.
st.markdown("<div style='height: 140px;'></div>", unsafe_allow_html=True)