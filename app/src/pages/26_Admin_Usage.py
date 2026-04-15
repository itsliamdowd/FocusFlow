import logging
logger = logging.getLogger(__name__)

import streamlit as st
from modules.nav import SideBarLinks

st.set_page_config(layout='wide')

SideBarLinks()

st.title('Monitor System-Wide Usage')
st.write('Jimmy can review platform-wide usage trends and activity levels from this page.')