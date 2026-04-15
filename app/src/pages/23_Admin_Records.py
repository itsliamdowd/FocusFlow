import logging
logger = logging.getLogger(__name__)

import streamlit as st
from modules.nav import SideBarLinks

st.set_page_config(layout='wide')

SideBarLinks()

st.title('Update Incorrect Records')
st.write('Jimmy can review and correct inaccurate system records from this page.')