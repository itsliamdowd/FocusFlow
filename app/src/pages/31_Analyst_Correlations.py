import logging
logger = logging.getLogger(__name__)

import streamlit as st
from modules.nav import SideBarLinks

st.set_page_config(layout='wide')

SideBarLinks()

st.title('Study Time vs Productivity Correlations')
st.write('Analyze how study time aligns with productivity outcomes across student activity data.')
