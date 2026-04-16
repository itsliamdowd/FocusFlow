import streamlit as st
from modules.nav import SideBarLinks

st.set_page_config(layout="wide")
SideBarLinks()

st.title("Analytics")
st.write("View your productivity trends, time breakdowns, and leaderboard stats.")

# Implement API later
productivity_scores = None
category_breakdown = None
leaderboard = None

# Top metrics
col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Productivity Score", "—")

with col2:
    st.metric("Total Focus Time", "—")

with col3:
    st.metric("Leaderboard Rank", "—")

st.divider()

# Productivity section
st.subheader("Productivity Over Time")
if productivity_scores:
    st.line_chart(productivity_scores)
else:
    st.info("No productivity data available yet.")

# Category breakdown section
st.subheader("Time Spent by Category")
if category_breakdown:
    st.bar_chart(category_breakdown)
else:
    st.info("No category breakdown available yet.")

# Leaderboard section - Not sure if we need it
st.subheader("Leaderboard")
if leaderboard:
    st.dataframe(leaderboard, use_container_width=True)
else:
    st.info("No leaderboard data available yet.")

st.divider()

st.subheader("Activity Logs")
st.write("This section can later show daily, weekly, or monthly activity summaries.")