import logging
logger = logging.getLogger(__name__)

import requests
import streamlit as st
from modules.api_client import get_api_base_url
from modules.nav import SideBarLinks

st.set_page_config(layout='wide')

SideBarLinks()

st.title('Filter Student Data by Major and Year')
st.write('Slice student productivity data by major and class year to compare cohorts.')

base_url = get_api_base_url()

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
    logger.exception('Failed to fetch institutions list for filtering page')

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
years = [1, 2, 3, 4]

col1, col2, col3 = st.columns(3)

with col1:
    selected_institution_label = st.selectbox('Institution', list(institutions.keys()))

with col2:
    selected_major = st.selectbox('Major', majors)

with col3:
    selected_year = st.selectbox('Year', years)

if st.button('Apply Filters', type='primary'):
    query_params = {'year': selected_year}

    if selected_major != 'All Majors':
        query_params['major'] = selected_major

    selected_institution_id = institutions.get(selected_institution_label)
    if selected_institution_id is not None:
        query_params['institution_id'] = selected_institution_id

    try:
        response = requests.get(
            f'{base_url}/analyst/activity',
            params=query_params,
            timeout=10,
        )
        response.raise_for_status()
        payload = response.json()
        activity = payload.get('activity', []) if isinstance(payload, dict) else []

        if isinstance(activity, list) and activity:
            st.dataframe(activity, use_container_width=True)
        elif isinstance(activity, list):
            st.info('No activity rows matched the selected filters.')
        else:
            st.warning('Unexpected response format returned by the API.')
    except requests.RequestException as exc:
        logger.exception('Failed to fetch analyst activity data')
        st.error(f'Could not load filtered activity data: {exc}')
