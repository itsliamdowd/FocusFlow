import logging
logger = logging.getLogger(__name__)

import requests
import streamlit as st
from modules.nav import SideBarLinks

st.set_page_config(layout='wide')

SideBarLinks()

st.title('Filter Student Data by Major and Year')
st.write('Slice student productivity data by major and class year to compare cohorts.')

institutions = [
	'All Institutions',
	'University of Toronto',
	'McGill University',
	'University of British Columbia',
	'University of Waterloo',
]
majors = ['Computer Science', 'Data Science']
years = [1, 2, 3, 4]

col1, col2, col3 = st.columns(3)

with col1:
	selected_institution = st.selectbox('Institution', institutions)

with col2:
	selected_major = st.selectbox('Major', majors)

with col3:
	selected_year = st.selectbox('Year', years)

if st.button('Apply Filters', type='primary'):
	query_params = {
		'major': selected_major,
		'year': selected_year,
	}

	if selected_institution != 'All Institutions':
		query_params['institution'] = selected_institution

	try:
		response = requests.get(
			'http://localhost:4000/analyst/activity',
			params=query_params,
			timeout=10,
		)
		response.raise_for_status()
		data = response.json()

		if isinstance(data, dict):
			if 'results' in data and isinstance(data['results'], list):
				st.dataframe(data['results'], use_container_width=True)
			else:
				st.dataframe([data], use_container_width=True)
		elif isinstance(data, list):
			st.dataframe(data, use_container_width=True)
		else:
			st.warning('No tabular data was returned for the selected filters.')
	except requests.RequestException as exc:
		logger.exception('Failed to fetch analyst activity data')
		st.error(f'Could not load filtered activity data: {exc}')
