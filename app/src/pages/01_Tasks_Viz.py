import logging
logger = logging.getLogger(__name__)
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
import plotly.express as px
from modules.nav import SideBarLinks

st.set_page_config(layout='wide')

# Call the SideBarLinks from the nav module in the modules directory
SideBarLinks()

st.title("Tasks")

# Add task
with st.form("add_task"):
    title = st.text_input("Task Title")
    category = st.selectbox("Category", ["School", "Work", "Extracurricular"])
    priority = st.selectbox("Priority", ["Low", "Medium", "High"])
    submitted = st.form_submit_button("Add Task")

    if submitted:
        st.session_state.tasks.append({
            "title": title,
            "category": category,
            "priority": priority
        })
        st.success("Task added!")

# Display tasks
st.subheader("Your Tasks")

for task in st.session_state.tasks:
    col1, col2 = st.columns([4,1])

    with col1:
        st.write(f"**{task['title']}** ({task['category']}, {task['priority']})")

    with col2:
        st.button("Delete", key= task["title"] + "_delete")