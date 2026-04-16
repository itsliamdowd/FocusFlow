import logging
logger = logging.getLogger(__name__)

import streamlit as st
from modules.nav import SideBarLinks

st.set_page_config(layout='wide')

SideBarLinks()

st.title('Export Student Activity Data')
st.write('Prepare and export student activity datasets for downstream reporting and analysis.')
