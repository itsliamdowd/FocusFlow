import logging
logger = logging.getLogger(__name__)

import streamlit as st
from modules.nav import SideBarLinks

st.set_page_config(layout='wide')

SideBarLinks()

st.title('Remove Duplicate Activity Logs')
st.write('Jimmy can review and clean duplicate activity logs from this page.')