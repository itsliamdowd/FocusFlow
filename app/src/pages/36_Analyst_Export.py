import logging
logger = logging.getLogger(__name__)

import csv
from io import StringIO

import requests
import streamlit as st
from modules.api_client import get_api_base_url
from modules.nav import SideBarLinks

st.set_page_config(layout='wide')

SideBarLinks()

base_url = get_api_base_url()

st.title('Export Student Activity Data')
st.write('Download filtered activity data for reporting and analysis.')

institutions = {'All Institutions': None}
try:
	institution_response = requests.get(f'{base_url}/analyst/institutions', timeout=10)
	institution_response.raise_for_status()
	payload = institution_response.json()
	if isinstance(payload, dict) and isinstance(payload.get('institutions'), list):
		institutions.update(
			{
				row.get('name', f"Institution {row.get('institution_id')}"): row.get('institution_id')
				for row in payload['institutions']
				if row.get('institution_id') is not None
			}
		)
except requests.RequestException:
	logger.exception('Failed to fetch institutions list for export page')

majors = [
	'All Majors',
	'Mathematics',
	'Health Sciences',
	'Engineering',
	'Business',
	'Computer Science',
	'Psychology',
	'Economics',
	'Law',
	'Philosophy',
	'Education',
	'Art',
	'Biology',
	'Chemistry',
	'Physics',
	'Sociology',
	'Political Science',
	'English',
	'Literature',
]

col1, col2 = st.columns(2)
with col1:
	selected_institution_label = st.selectbox('Institution', list(institutions.keys()))
with col2:
	selected_major = st.selectbox('Major', majors)

if st.button('Export Data', type='primary'):
	try:
		query_params = {}

		selected_institution_id = institutions.get(selected_institution_label)
		if selected_institution_id is not None:
			query_params['institution_id'] = selected_institution_id

		if selected_major != 'All Majors':
			query_params['major'] = selected_major

		response = requests.get(f'{base_url}/analyst/export', params=query_params, timeout=10)
		response.raise_for_status()
		rows = response.json().get('export', [])
		st.caption(f'Exporting {len(rows)} records')
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
