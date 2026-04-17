import logging
logger = logging.getLogger(__name__)

import streamlit as st
import requests
from modules.nav import SideBarLinks

st.set_page_config(layout='wide')
SideBarLinks()

BASE_URL = 'http://api:4000/professor'
professor_id = st.session_state.get('user_id', 1)

st.title('Professor Student Roster')

response = requests.get(f'{BASE_URL}/courses', params={'professor_id': professor_id})
if response.status_code != 200:
    st.error('Could not load courses. Please make sure the API server is running.')
    st.stop()

courses = response.json().get('courses', [])
if not courses:
    st.info('You have no courses yet. Create one in the Manage My Courses page first.')
    st.stop()

course_options = [f"{course['course_code']} — {course['title']} (ID {course['course_id']})" for course in courses]
selected_index = st.selectbox('Select a course', list(range(len(course_options))), format_func=lambda i: course_options[i], key='professor_roster_course_index')
selected_course = courses[selected_index]
selected_course_id = selected_course['course_id']

st.subheader(f"Roster for {selected_course['course_code']} — {selected_course['title']}")

students_response = requests.get(f'{BASE_URL}/courses/{selected_course_id}/students')
if students_response.status_code != 200:
    st.error('Could not load student roster for the selected course.')
    st.stop()

students = students_response.json().get('students', [])
if not students:
    st.info('No students are currently enrolled in this course.')
else:
    for student in students:
        cols = st.columns([5, 3, 2])
        cols[0].write(f"**{student['first_name']} {student['last_name']}**")
        cols[0].write(student['email'])
        cols[1].write(f"Total time logged: {student['total_time_logged']} sec")
        if cols[2].button('Remove', key=f"remove_{selected_course_id}_{student['user_id']}"):
            delete_response = requests.delete(
                f'{BASE_URL}/courses/{selected_course_id}/students',
                json={'user_id': student['user_id']}
            )
            if delete_response.status_code == 200:
                st.success('Student removed successfully.')
                st.experimental_rerun()
            else:
                st.error('Failed to remove student.')

st.divider()
with st.expander('Add a student to this course'):
    new_student_id = st.number_input('Student User ID', min_value=1, step=1, value=1, key='add_student_user_id')
    if st.button('Add Student', key=f'add_student_{selected_course_id}'):
        add_response = requests.post(
            f'{BASE_URL}/courses/{selected_course_id}/students',
            json={'user_id': int(new_student_id)}
        )
        if add_response.status_code == 201:
            st.success('Student added successfully.')
            st.experimental_rerun()
        else:
            st.error('Failed to add student. Please verify the user ID and try again.')
