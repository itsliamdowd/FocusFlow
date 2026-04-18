import logging
logger = logging.getLogger(__name__)

import requests
import streamlit as st
from modules.nav import SideBarLinks

st.set_page_config(layout='wide')

SideBarLinks()

st.title('Time Breakdown by Category')
st.write('Review how time is distributed across productivity categories and activity types.')

user_id = st.number_input('User ID', min_value=1, step=1, value=1)

if st.button('Analyze', type='primary'):
	try:
		response = requests.get(
			'http://localhost:4000/analyst/breakdown',
			params={'user_id': int(user_id)},
			timeout=10,
		)
		response.raise_for_status()
		rows = response.json()
		st.dataframe(rows, use_container_width=True)

		chart_data = {
			row['category']: row['total_minutes']
			for row in rows
		}
		st.bar_chart(chart_data)
	except requests.RequestException as exc:
		logger.exception('Failed to fetch analyst category breakdown')
		st.error(f'Could not load category breakdown data: {exc}')
