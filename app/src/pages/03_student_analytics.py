import streamlit as st
import pandas as pd
import requests
from modules.nav import SideBarLinks

st.set_page_config(layout="wide")
SideBarLinks()

BASE_URL = 'http://api:4000/student'
user_id = st.session_state.get('user_id', 1)
institution_id = st.session_state.get('institution_id', 1)

st.title("Analytics")
st.write("View your productivity trends, time breakdowns, and leaderboard stats.")

productivity_scores = []
activity_data = []
leaderboard = []

try:
    prod_response = requests.get(f"{BASE_URL}/productivity", params={"user_id": user_id})
    if prod_response.status_code == 200:
        productivity_scores = prod_response.json().get('productivity', [])

    activity_response = requests.get(f"{BASE_URL}/activity", params={"user_id": user_id})
    if activity_response.status_code == 200:
        activity_data = activity_response.json().get('activity', [])

    leaderboard_response = requests.get(f"{BASE_URL}/leaderboard", params={"institution_id": institution_id})
    if leaderboard_response.status_code == 200:
        leaderboard = leaderboard_response.json().get('leaderboard', [])
except requests.exceptions.RequestException as exc:
    st.error(f"Unable to reach analytics services: {exc}")

# Top metrics
col1, col2, col3 = st.columns(3)

with col1:
    if productivity_scores:
        latest_score = productivity_scores[-1].get('score', '—')
        st.metric("Productivity Score", latest_score)
    else:
        st.metric("Productivity Score", "—")

with col2:
    total_focus = sum(item.get('total_duration', 0) for item in activity_data)
    st.metric("Total Focus Time", f"{total_focus} min")

with col3:
    if leaderboard:
        matching = next((row for row in leaderboard if row.get('user_id') == user_id), None)
        rank = 1 + sum(1 for row in leaderboard if row.get('avg_score', 0) > (matching.get('avg_score', 0) if matching else 0))
        st.metric("Leaderboard Rank", rank)
    else:
        st.metric("Leaderboard Rank", "—")

st.divider()

# Productivity section
st.subheader("Productivity Over Time")
if productivity_scores:
    prod_df = pd.DataFrame(productivity_scores)
    if 'week_start_date' in prod_df.columns:
        prod_df['week_start_date'] = pd.to_datetime(prod_df['week_start_date'])
        prod_df = prod_df.sort_values('week_start_date')
        st.line_chart(prod_df.set_index('week_start_date')['score'])
    else:
        st.line_chart(prod_df)
else:
    st.info("No productivity data available yet.")

# Category breakdown section
st.subheader("Time Spent by Category")
if activity_data:
    activity_df = pd.DataFrame(activity_data)
    if 'category' in activity_df.columns and 'total_duration' in activity_df.columns:
        breakdown = activity_df.groupby('category')['total_duration'].sum()
        st.bar_chart(breakdown)
    else:
        st.write(activity_df)
else:
    st.info("No category breakdown available yet.")

# Leaderboard section
st.subheader("Leaderboard")
if leaderboard:
    leaderboard_df = pd.DataFrame(leaderboard)
    if not leaderboard_df.empty:
        st.dataframe(leaderboard_df.sort_values(by='avg_score', ascending=False), use_container_width=True)
    else:
        st.info("No leaderboard data available yet.")
else:
    st.info("No leaderboard data available yet.")

st.divider()

st.subheader("Activity Logs")
if activity_data:
    st.dataframe(pd.DataFrame(activity_data), use_container_width=True)
else:
    st.write("This section can later show daily, weekly, or monthly activity summaries.")