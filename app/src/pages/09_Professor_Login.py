import logging
logger = logging.getLogger(__name__)

import streamlit as st
from modules.api_client import api_get, show_api_error
from modules.nav import SideBarLinks

st.set_page_config(layout='wide')
SideBarLinks(show_home=True)

st.title('Professor Login')

try:
    professors = api_get('/professor/users').get('professors', [])
    if not professors:
        st.info('No professors found in the database.')
        st.stop()

    prof_options = {f"{p['first_name']} {p['last_name']} (ID {p['user_id']})": p for p in professors}
    selected_label = st.selectbox('Select your profile', list(prof_options.keys()))
    selected = prof_options[selected_label]

    st.write(f"**Email:** {selected['email']}")

    if st.button('Continue', type='primary', use_container_width=True):
        st.session_state['authenticated'] = True
        st.session_state['role'] = 'professor'
        st.session_state['first_name'] = selected['first_name']
        st.session_state['user_id'] = selected['user_id']
        st.session_state['institution'] = selected.get('institution',1)
        st.switch_page('pages/10_Professor_Home.py')

except Exception as exc:
    show_api_error(exc)