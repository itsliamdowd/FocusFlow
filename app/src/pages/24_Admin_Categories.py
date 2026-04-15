import logging
logger = logging.getLogger(__name__)

import streamlit as st
from modules.nav import SideBarLinks

st.set_page_config(layout='wide')

SideBarLinks()

st.title('Manage Activity Categories')
st.write('Jimmy can create, edit, and organize activity categories from this page.')