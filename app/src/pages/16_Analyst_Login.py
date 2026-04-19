import logging
logger = logging.getLogger(__name__)

import streamlit as st
import requests
from modules.nav import SideBarLinks

st.set_page_config(layout='wide')
SideBarLinks(show_home=True)

st.title('Data Analyst Login')

try:
    response = requests.get('http://web-api:4000/analyst/users', timeout=10)
    if response.status_code != 200:
        st.error('Could not load analyst list from the API.')
        st.stop()

    analysts = response.json().get('analysts', [])
    if not analysts:
        st.info('No analysts found in the database.')
        st.stop()

    analyst_options = {
        f"{a['first_name']} {a['last_name']} (ID {a['user_id']})": a
        for a in analysts
    }

    selected_label = st.selectbox('Select your profile', list(analyst_options.keys()))
    selected = analyst_options[selected_label]

    st.write(f"**Email:** {selected.get('email', 'N/A')}")

    if st.button('Continue', type='primary', use_container_width=True):
        st.session_state['authenticated'] = True
        st.session_state['role'] = 'data analyst'
        st.session_state['first_name'] = selected['first_name']
        st.session_state['user_id'] = selected['user_id']
        st.session_state['institution_id'] = selected.get('institution_id', 1)
        st.switch_page('pages/17_Data_Analyst_Home.py')

except Exception as e:
    st.error(f'Could not connect to the API: {e}')