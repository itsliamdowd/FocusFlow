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

st.title('Student Roster')

response = requests.get(f'{BASE_URL}/courses', params={'professor_id': professor_id})
if response.status_code != 200:
    st.error('Could not load courses. Please make sure the API server is running.')
    st.stop()

courses = response.json().get('courses', [])
if not courses:
    st.info('You have no courses yet. Create one in the Manage My Courses page first.')
    st.stop()

course_options = [f"{course['course_code']} — {course['title']}" for course in courses]
selected_index = st.selectbox('Select a course', list(range(len(course_options))), format_func=lambda i: course_options[i], key='professor_roster_course_index')
selected_course = courses[selected_index]
selected_course_id = selected_course['course_id']

st.subheader(f"{selected_course['course_code']} — {selected_course['title']}")

students_response = requests.get(f'{BASE_URL}/courses/{selected_course_id}/students')
if students_response.status_code != 200:
    st.error('Could not load student roster for the selected course.')
    st.stop()

students = students_response.json().get('students', [])
if not students:
    st.info('No students are currently enrolled in this course.')
else:
    roster_df = pd.DataFrame(students)
    roster_df["name"] = roster_df["first_name"] + " " + roster_df["last_name"]
    roster_df["minutes_logged"] = (
        pd.to_numeric(roster_df.get("total_time_logged", 0), errors="coerce").fillna(0) / 60
    ).round(1)
    st.dataframe(
        roster_df[[c for c in ["user_id", "name", "email", "minutes_logged"] if c in roster_df.columns]],
        hide_index=True,
        use_container_width=True,
    )

    remove_options = {
        f"{row['name']} (ID {int(row['user_id'])})": int(row["user_id"])
        for _, row in roster_df.iterrows()
    }
    selected_remove = st.selectbox(
        "Select student to remove",
        options=["None"] + list(remove_options.keys()),
        index=0,
        key=f"remove_student_select_{selected_course_id}",
    )
    if st.button("Remove Selected Student", disabled=selected_remove == "None"):
        delete_response = requests.delete(
            f'{BASE_URL}/courses/{selected_course_id}/students',
            json={'user_id': remove_options[selected_remove]}
        )
        if delete_response.status_code == 200:
            st.success('Student removed successfully.')
            st.rerun()
        else:
            st.error('Failed to remove student.')

    st.divider()
    st.subheader('Time Distribution')

    dist_response = requests.get(f'{BASE_URL}/courses/{selected_course_id}/distribution')
    if dist_response.status_code == 200:
        dist_data = dist_response.json().get('distribution', [])
        if dist_data:
            df = pd.DataFrame(dist_data)
            df['name'] = df['first_name'] + ' ' + df['last_name']
            df['minutes'] = (pd.to_numeric(df['total_time'], errors='coerce').fillna(0) / 60).round(1)
            df = df[['name', 'minutes']].set_index('name')
            st.bar_chart(df, y='minutes', y_label='Minutes Logged', x_label='Student')
        else:
            st.info('No time data logged yet for this course.')
    else:
        st.error('Could not load distribution data.')

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
            st.rerun()
        else:
            st.error('Failed to add student. Please verify the user ID and try again.')