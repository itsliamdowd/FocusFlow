import logging
logger = logging.getLogger(__name__)

import streamlit as st
from modules.nav import SideBarLinks

st.set_page_config(layout='wide')

SideBarLinks()

st.title('Time Breakdown by Category')
st.write('Review how time is distributed across productivity categories and activity types.')
