import logging
logger = logging.getLogger(__name__)

import streamlit as st
import requests
from modules.nav import SideBarLinks

st.set_page_config(layout='wide')
SideBarLinks(show_home=True)

st.title('Student Login')

try:
    response = requests.get('http://web-api:4000/student/users', timeout=10)
    if response.status_code != 200:
        st.error('Could not load student list from the API.')
        st.stop()

    students = response.json().get('students', [])
    if not students:
        st.info('No students found in the database.')
        st.stop()

    student_options = {
        f"{s['first_name']} {s['last_name']} (ID {s['user_id']})": s
        for s in students
    }

    selected_label = st.selectbox('Select your profile', list(student_options.keys()))
    selected = student_options[selected_label]

    st.write(f"**Email:** {selected.get('email', 'N/A')}")
    st.write(f"**Major:** {selected.get('major', 'N/A')}")
    st.write(f"**Year:** {selected.get('year', 'N/A')}")

    if st.button('Continue', type='primary', use_container_width=True):
        st.session_state['authenticated'] = True
        st.session_state['role'] = 'student'
        st.session_state['first_name'] = selected['first_name']
        st.session_state['user_id'] = selected['user_id']
        st.session_state['institution_id'] = selected.get('institution_id', 1)
        st.switch_page('pages/00_Student_Home.py')

except Exception as e:
    st.error(f'Could not connect to the API: {e}')