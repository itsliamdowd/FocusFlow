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

st.title('Manage Assignments')
st.write('Create, review, and remove assignments for your courses.')

courses = []
try:
    courses_response = requests.get(f'{BASE_URL}/courses', params={'professor_id': professor_id})
    if courses_response.status_code == 200:
        courses = courses_response.json().get('courses', [])
    else:
        st.error(courses_response.json().get('error', 'Unable to load courses.'))
except requests.exceptions.RequestException as exc:
    st.error(f'Could not connect to the professor service: {exc}')

if not courses:
    st.info('No courses are currently assigned to you. Create a course first on My Courses.')
    st.stop()

course_options = [f"{course['course_code']} — {course['title']}" for course in courses]
selected_index = st.selectbox('Select a course', list(range(len(courses))), format_func=lambda i: course_options[i], key='professor_assignment_course_id')
selected_course = courses[selected_index]
selected_course_id = selected_course['course_id']

st.write(f"### Course: {selected_course['course_code']} — {selected_course['title']}")

assignments = []
try:
    assignments_response = requests.get(f'{BASE_URL}/courses/{selected_course_id}/assignments')
    if assignments_response.status_code == 200:
        assignments = assignments_response.json().get('assignments', [])
    else:
        st.error(assignments_response.json().get('error', 'Unable to load assignments.'))
except requests.exceptions.RequestException as exc:
    st.error(f'Could not connect to the professor service: {exc}')

if not assignments:
    st.info('No assignments have been created for this course yet.')
else:
    assignments_df = pd.DataFrame(assignments)
    display_cols = [
        col for col in ["assignment_id", "title", "due_date", "time_benchmark", "description"]
        if col in assignments_df.columns
    ]
    st.dataframe(assignments_df[display_cols], hide_index=True, use_container_width=True)

    delete_options = {
        f"{row.get('title', 'Untitled')} (ID {row.get('assignment_id')})": row.get("assignment_id")
        for _, row in assignments_df.iterrows()
    }
    selected_delete_assignment = st.selectbox(
        "Select assignment to delete",
        options=["None"] + list(delete_options.keys()),
        index=0,
        key=f"assignment_delete_{selected_course_id}",
    )
    if st.button("Delete Selected Assignment", disabled=selected_delete_assignment == "None"):
        try:
            delete_response = requests.delete(
                f"{BASE_URL}/assignments/{delete_options[selected_delete_assignment]}"
            )
            if delete_response.status_code == 200:
                st.success('Assignment deleted successfully.')
                st.rerun()
            else:
                st.error(delete_response.json().get('error', 'Failed to delete assignment.'))
        except requests.exceptions.RequestException as exc:
            st.error(f'Failed to reach the assignment service: {exc}')

st.divider()

st.subheader('Create a New Assignment')
with st.form('new_assignment_form'):
    title = st.text_input('Assignment Title')
    description = st.text_area('Description')
    due_date = st.date_input('Due Date')
    time_benchmark = st.text_input('Suggested Study Time (minutes)')
    submitted = st.form_submit_button('Create Assignment')

    if submitted:
        if not title:
            st.error('Assignment title is required.')
        else:
            payload = {
                'title': title,
                'description': description,
                'due_date': str(due_date),
                'time_benchmark': time_benchmark or None
            }
            try:
                create_response = requests.post(f'{BASE_URL}/courses/{selected_course_id}/assignments', json=payload)
                if create_response.status_code == 201:
                    st.success('Assignment created successfully.')
                    st.rerun()
                else:
                    st.error(create_response.json().get('error', 'Failed to create assignment.'))
            except requests.exceptions.RequestException as exc:
                st.error(f'Failed to connect to the assignment service: {exc}')
