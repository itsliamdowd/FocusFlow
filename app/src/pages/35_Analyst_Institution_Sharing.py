import logging
logger = logging.getLogger(__name__)

import requests
import streamlit as st
from modules.nav import SideBarLinks

st.set_page_config(layout='wide')

SideBarLinks()

st.title('Data Sharing by Institution')
st.write('Monitor participation and data-sharing behavior across institutions.')

if st.button('Load Data', type='primary'):
	try:
		response = requests.get('http://localhost:4000/analyst/shared', timeout=10)
		response.raise_for_status()
		data = response.json()
		st.dataframe(data, use_container_width=True)
	except requests.RequestException as exc:
		logger.exception('Failed to fetch shared institution activity data')
		st.error(f'Could not load shared activity data: {exc}')
