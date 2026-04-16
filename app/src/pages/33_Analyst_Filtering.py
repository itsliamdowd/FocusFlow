import logging
logger = logging.getLogger(__name__)

import streamlit as st
from modules.nav import SideBarLinks

st.set_page_config(layout='wide')

SideBarLinks()

st.title('Filter Student Data by Major and Year')
st.write('Slice student productivity data by major and class year to compare cohorts.')
