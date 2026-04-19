import logging
logger = logging.getLogger(__name__)

import pandas as pd
import requests
import streamlit as st
from modules.api_client import get_api_base_url
from modules.nav import SideBarLinks

st.set_page_config(layout='wide')

SideBarLinks()

st.title('Time Breakdown by Category')
st.write('Review how time is distributed across productivity categories and activity types.')

user_id = st.number_input('User ID', min_value=1, step=1, value=1)

if st.button('Analyze', type='primary'):
	base_url = get_api_base_url()
	try:
		response = requests.get(
			f'{base_url}/analyst/breakdown',
			params={'user_id': int(user_id)},
			timeout=10,
		)
		response.raise_for_status()
		payload = response.json()
		rows = payload.get('breakdown', []) if isinstance(payload, dict) else []
		if not isinstance(rows, list):
			st.warning('Unexpected response format returned by the API.')
		elif not rows:
			st.info('No category activity found for this user.')
		else:
			st.caption(f'Showing breakdown for User ID {int(user_id)}.')
			summary_df = pd.DataFrame(rows)
			if 'category' in summary_df.columns and 'total_minutes' in summary_df.columns:
				summary_df = summary_df[['category', 'total_minutes']].copy()
				summary_df['total_minutes'] = pd.to_numeric(summary_df['total_minutes'], errors='coerce').fillna(0)
				st.dataframe(summary_df, use_container_width=True)
				st.bar_chart(summary_df.set_index('category')[['total_minutes']])
			else:
				st.warning('Breakdown data is missing category or total_minutes fields.')
	except (requests.RequestException, TypeError, ValueError, KeyError) as exc:
		logger.exception('Failed to fetch analyst category breakdown')
		st.error(f'Could not load category breakdown data: {exc}')
