import logging
logger = logging.getLogger(__name__)

import requests
import streamlit as st
from modules.api_client import get_api_base_url
from modules.nav import SideBarLinks

st.set_page_config(layout='wide')

SideBarLinks()

st.title('Data Sharing by Institution')
st.write('Monitor participation and data-sharing behavior across institutions.')

if st.button('Load Data', type='primary'):
	try:
		base_url = get_api_base_url()
		response = requests.get(f'{base_url}/analyst/shared', timeout=10)
		response.raise_for_status()
		payload = response.json()
		rows = payload.get('shared', []) if isinstance(payload, dict) else []
		if isinstance(rows, list):
			st.dataframe(rows, use_container_width=True)
		else:
			st.warning('Unexpected response format returned by the API.')
	except requests.RequestException as exc:
		logger.exception('Failed to fetch shared institution activity data')
		st.error(f'Could not load shared activity data: {exc}')
