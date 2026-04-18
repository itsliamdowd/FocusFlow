import logging
logger = logging.getLogger(__name__)

import requests
import streamlit as st
from modules.nav import SideBarLinks

st.set_page_config(layout='wide')

SideBarLinks()

st.title('Export Student Activity Data')
st.write('Prepare and export student activity datasets for downstream reporting and analysis.')

if st.button('Load Data', type='primary'):
	try:
		response = requests.get('http://localhost:4000/analyst/shared', timeout=10)
		response.raise_for_status()
		rows = response.json()
		st.dataframe(rows, use_container_width=True)
	except requests.RequestException as exc:
		logger.exception('Failed to fetch institution sharing data')
		st.error(f'Could not load sharing data: {exc}')
