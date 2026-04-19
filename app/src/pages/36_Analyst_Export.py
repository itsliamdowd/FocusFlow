import logging
logger = logging.getLogger(__name__)

import csv
from io import StringIO

import requests
import streamlit as st
from modules.nav import SideBarLinks

st.set_page_config(layout='wide')

SideBarLinks()

st.title('Export Student Activity Data')
st.write('Download filtered activity data for reporting and analysis.')

if st.button('Export Data', type='primary'):
	try:
		response = requests.get('http://localhost:4000/analyst/export', timeout=10)
		response.raise_for_status()
		rows = response.json()
		st.dataframe(rows, use_container_width=True)

		csv_buffer = StringIO()
		if rows and isinstance(rows, list) and isinstance(rows[0], dict):
			writer = csv.DictWriter(csv_buffer, fieldnames=rows[0].keys())
			writer.writeheader()
			writer.writerows(rows)
		else:
			csv_buffer.write('No data returned\n')

		st.download_button(
			label='Download CSV',
			data=csv_buffer.getvalue(),
			file_name='student_activity_export.csv',
			mime='text/csv',
		)
	except requests.RequestException as exc:
		logger.exception('Failed to fetch export activity data')
		st.error(f'Could not load export data: {exc}')
