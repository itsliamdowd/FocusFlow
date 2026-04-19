import logging
logger = logging.getLogger(__name__)

import streamlit as st
from modules.nav import SideBarLinks

st.set_page_config(layout='wide')

SideBarLinks()

st.title('Data Analyst Console')
st.write('Select a task to get started.')

if st.button('View Study Time vs Productivity Correlations',
			 type='primary',
			 use_container_width=True):
	st.switch_page('pages/31_Analyst_Correlations.py')

if st.button('Flag Concerning Trends',
			 type='primary',
			 use_container_width=True):
	st.switch_page('pages/32_Analyst_Trend_Flags.py')

if st.button('Filter Student Data by Major and Year',
			 type='primary',
			 use_container_width=True):
	st.switch_page('pages/33_Analyst_Filtering.py')

if st.button('View Time Breakdown by Category',
			 type='primary',
			 use_container_width=True):
	st.switch_page('pages/34_Analyst_Category_Breakdown.py')

if st.button('Check Data Sharing by Institution',
			 type='primary',
			 use_container_width=True):
	st.switch_page('pages/35_Analyst_Institution_Sharing.py')

if st.button('Export Student Activity Data',
			 type='primary',
			 use_container_width=True):
	st.switch_page('pages/36_Analyst_Export.py')

