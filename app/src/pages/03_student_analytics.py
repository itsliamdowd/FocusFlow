import logging
logger = logging.getLogger(__name__)

import streamlit as st
import pandas as pd
import requests
from modules.nav import SideBarLinks

st.set_page_config(layout="wide")
SideBarLinks()

BASE_URL = 'http://api:4000/student'
user_id = st.session_state.get('user_id', 25)
institution_id = st.session_state.get('institution_id', 1)
role = st.session_state.get('role', 'student')

st.title("Analytics")
st.write("View your productivity trends, time breakdowns, and leaderboard stats.")


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


productivity_scores = []
activity_data = []
leaderboard = []
load_errors = []

try:
    prod_response = requests.get(
        f"{BASE_URL}/productivity",
        params={"user_id": user_id},
        headers=build_headers(),
        timeout=10
    )
    if prod_response.status_code == 200:
        productivity_scores = prod_response.json().get('productivity', [])
    else:
        try:
            load_errors.append(prod_response.json().get('error', 'Unable to load productivity data.'))
        except ValueError:
            load_errors.append('Unable to load productivity data.')
except requests.exceptions.RequestException as exc:
    load_errors.append(str(exc))

try:
    activity_response = requests.get(
        f"{BASE_URL}/activity",
        params={"user_id": user_id},
        headers=build_headers(),
        timeout=10
    )
    if activity_response.status_code == 200:
        activity_data = activity_response.json().get('activity', [])
    else:
        try:
            load_errors.append(activity_response.json().get('error', 'Unable to load activity data.'))
        except ValueError:
            load_errors.append('Unable to load activity data.')
except requests.exceptions.RequestException as exc:
    load_errors.append(str(exc))

try:
    leaderboard_response = requests.get(
        f"{BASE_URL}/leaderboard",
        params={"institution_id": institution_id},
        headers=build_headers(),
        timeout=10
    )
    if leaderboard_response.status_code == 200:
        leaderboard = leaderboard_response.json().get('leaderboard', [])
    else:
        try:
            load_errors.append(leaderboard_response.json().get('error', 'Unable to load leaderboard data.'))
        except ValueError:
            load_errors.append('Unable to load leaderboard data.')
except requests.exceptions.RequestException as exc:
    load_errors.append(str(exc))

for error in load_errors:
    st.warning(error)

# Top metrics
col1, col2, col3 = st.columns(3)

with col1:
    if productivity_scores:
        latest_score = productivity_scores[-1].get('score', '—')
        st.metric("Productivity Score", latest_score)
    else:
        st.metric("Productivity Score", "—")

with col2:
    total_focus = sum(
        int(item.get('total_duration') or 0)
        for item in activity_data
    )
    st.metric("Total Focus Time", f"{total_focus} min")

with col3:
    if leaderboard:
        matching = next((row for row in leaderboard if row.get('user_id') == user_id), None)
        if matching:
            rank = 1 + sum(
                1 for row in leaderboard
                if row.get('avg_score', 0) > matching.get('avg_score', 0)
            )
            st.metric("Leaderboard Rank", rank)
        else:
            st.metric("Leaderboard Rank", "—")
    else:
        st.metric("Leaderboard Rank", "—")

st.divider()

# Productivity section
st.subheader("Productivity Over Time")
if productivity_scores:
    prod_df = pd.DataFrame(productivity_scores)
    if 'week_start_date' in prod_df.columns and 'score' in prod_df.columns:
        prod_df['week_start_date'] = pd.to_datetime(prod_df['week_start_date'])
        prod_df = prod_df.sort_values('week_start_date')
        st.line_chart(prod_df.set_index('week_start_date')['score'])
        st.dataframe(prod_df, use_container_width=True)
    else:
        st.dataframe(prod_df, use_container_width=True)
else:
    st.info("No productivity data available yet.")

# Category breakdown section
st.subheader("Time Spent by Category")
if activity_data:
    activity_df = pd.DataFrame(activity_data)
    if 'category' in activity_df.columns and 'total_duration' in activity_df.columns:
        breakdown = activity_df.groupby('category')['total_duration'].sum()
        st.bar_chart(breakdown)
    st.dataframe(activity_df, use_container_width=True)
else:
    st.info("No category breakdown available yet.")

# Leaderboard section
st.subheader("Leaderboard")
if leaderboard:
    leaderboard_df = pd.DataFrame(leaderboard)
    if not leaderboard_df.empty and 'avg_score' in leaderboard_df.columns:
        st.dataframe(
            leaderboard_df.sort_values(by='avg_score', ascending=False),
            use_container_width=True
        )
    else:
        st.dataframe(leaderboard_df, use_container_width=True)
else:
    st.info("No leaderboard data available yet.")