import logging
logger = logging.getLogger(__name__)

import streamlit as st
import requests
from modules.nav import SideBarLinks

st.set_page_config(layout='wide')
SideBarLinks()

BASE_URL = 'http://api:4000/professor'

professor_id = st.session_state.get('user_id', 1)

st.title('My Courses')

response = requests.get(f'{BASE_URL}/courses', params={'professor_id': professor_id})

if response.status_code == 200:
    courses = response.json().get('courses', [])
    if not courses:
        st.info('You have no courses yet.')
    for course in courses:
        with st.expander(f"{course['course_code']} — {course['title']}"):
            st.write(f"**Course ID:** {course['course_id']}")
            col1, col2 = st.columns([1, 5])
            with col1:
                if st.button('Delete', key=f"del_{course['course_id']}"):
                    del_response = requests.delete(f"{BASE_URL}/courses/{course['course_id']}")
                    if del_response.status_code == 200:
                        st.success('Course deleted.')
                        st.rerun()
                    else:
                        st.error('Failed to delete course.')
else:
    st.error('Could not load courses.')

st.divider()
st.subheader('Create a New Course')

with st.form('create_course_form'):
    title = st.text_input('Course Title')
    course_code = st.text_input('Course Code (e.g. CS 3200)')
    department_id = st.number_input('Department ID', min_value=1, step=1, value=1)
    submitted = st.form_submit_button('Create Course')

    if submitted:
        if not title or not course_code:
            st.error('Title and course code are required.')
        else:
            payload = {
                'professor_id': professor_id,
                'department_id': int(department_id),
                'title': title,
                'course_code': course_code
            }
            create_response = requests.post(f'{BASE_URL}/courses', json=payload)
            if create_response.status_code == 201:
                st.success(f'Course "{title}" created successfully.')
                st.rerun()
            else:
                st.error('Failed to create course.')