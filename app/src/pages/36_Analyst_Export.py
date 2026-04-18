import logging
logger = logging.getLogger(__name__)

import requests
import streamlit as st
from modules.api_client import get_api_base_url
from modules.nav import SideBarLinks

st.set_page_config(layout='wide')

SideBarLinks()

st.title('Export Student Activity Data')
st.write('Prepare and export student activity datasets for downstream reporting and analysis.')

if st.button('Load Data', type='primary'):
	try:
		base_url = get_api_base_url()
		response = requests.get(f'{base_url}/analyst/export', timeout=10)
		response.raise_for_status()
		payload = response.json()
		rows = payload.get('export', []) if isinstance(payload, dict) else []
		if isinstance(rows, list):
			st.dataframe(rows, use_container_width=True)
		else:
			st.warning('Unexpected response format returned by the API.')
	except requests.RequestException as exc:
		logger.exception('Failed to fetch export activity data')
		st.error(f'Could not load export data: {exc}')
