import logging
logger = logging.getLogger(__name__)

import streamlit as st
from modules.nav import SideBarLinks

st.set_page_config(layout='wide')

SideBarLinks()

st.title('Flag Concerning Trends')
st.write('Identify and flag concerning productivity patterns that may require intervention.')
