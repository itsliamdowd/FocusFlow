import logging
logger = logging.getLogger(__name__)
import streamlit as st
import time
import pandas as pd
import pydeck as pdk
from urllib.error import URLError
from modules.nav import SideBarLinks

st.set_page_config(layout='wide')

SideBarLinks()

# set up the page
st.title("Timer")
st.write("Set a timer to stay on task and track your habits!")

# State of the Timer
if "time_left" not in st.session_state:
    st.session_state.time_left = 1800  # 30 min default

if "running" not in st.session_state:
    st.session_state.running = False

def format_time(sec):
    return f"{sec//60:02d}:{sec%60:02d}"

st.subheader("Pomodoro Timer")

st.metric("Time", format_time(st.session_state.time_left))

col1, col2 = st.columns(2)

with col1:
    if st.button("Start"):
        st.session_state.running = True

with col2:
    if st.button("Reset"):
        st.session_state.running = False
        st.session_state.time_left = 1800

# timer loop
if st.session_state.running:
    time.sleep(1)
    st.session_state.time_left -= 1
    st.rerun()