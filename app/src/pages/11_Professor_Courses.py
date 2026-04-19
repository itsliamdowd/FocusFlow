import logging
logger = logging.getLogger(__name__)

import streamlit as st
import requests
import pandas as pd
from modules.nav import SideBarLinks

st.set_page_config(layout='wide')
SideBarLinks()

BASE_URL = 'http://web-api:4000/professor'

professor_id = st.session_state.get('user_id', 1)

st.title('My Courses')
st.write("Create courses and manage your existing catalog.")

response = requests.get(f'{BASE_URL}/courses', params={'professor_id': professor_id})

if response.status_code == 200:
    courses = response.json().get('courses', [])
else:
    st.error('Could not load courses.')
    st.stop()

if not courses:
    st.info('You have no courses yet.')
else:
    total_courses = len(courses)
    st.metric("Total Courses", total_courses)
    course_df = pd.DataFrame(courses)
    display_cols = [c for c in ["course_id", "course_code", "title", "department_id"] if c in course_df.columns]
    st.dataframe(course_df[display_cols], hide_index=True, use_container_width=True)

    delete_options = {
        f"{course['course_code']} — {course['title']} (ID {course['course_id']})": course["course_id"]
        for course in courses
    }
    selected_delete_label = st.selectbox(
        "Select course to delete",
        options=["None"] + list(delete_options.keys()),
        index=0,
        key="prof_delete_course_select",
    )
    if st.button("Delete Selected Course", type="secondary", disabled=selected_delete_label == "None"):
        selected_course_id = delete_options[selected_delete_label]
        del_response = requests.delete(f"{BASE_URL}/courses/{selected_course_id}")
        if del_response.status_code == 200:
            st.success('Course deleted.')
            st.rerun()
        else:
            st.error('Failed to delete course.')

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