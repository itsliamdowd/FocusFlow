import logging
logger = logging.getLogger(__name__)

import streamlit as st
import requests
from modules.nav import SideBarLinks

st.set_page_config(layout='wide')
SideBarLinks(show_home=True)

st.title('System Administrator Login')

try:
    with st.spinner('Loading...'):
        response = requests.get('http://web-api:4000/admin/admins', timeout=10)
        if response.status_code != 200:
            st.error('Could not load admin list from the API.')
            st.stop()

        admins = response.json().get('admins', [])
    if not admins:
        st.info('No administrmators found in the database.')
        st.stop()

    admin_options = {
        f"{a['first_name']} {a['last_name']} (ID {a['user_id']})": a
        for a in admins
    }

    selected_label = st.selectbox('Select your profile', list(admin_options.keys()))
    selected = admin_options[selected_label]

    st.write(f"**Email:** {selected.get('email', 'N/A')}")

    if st.button('Continue', type='primary', use_container_width=True):
        st.session_state['authenticated'] = True
        st.session_state['role'] = 'system admin'
        st.session_state['first_name'] = selected['first_name']
        st.session_state['user_id'] = selected['user_id']
        st.session_state['institution_id'] = selected.get('institution_id', 1)
        st.switch_page('pages/20_Admin_Home.py')

except Exception as e:
    st.error(f'Could not connect to the API: {e}')