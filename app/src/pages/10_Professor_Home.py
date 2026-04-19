import logging
logger = logging.getLogger(__name__)

import streamlit as st
from modules.nav import SideBarLinks

st.set_page_config(layout='wide')

SideBarLinks()

st.title(f"Welcome, {st.session_state['first_name']}.")
st.write("Run your teaching workflow from one place.")

st.markdown(
    """
    <style>
        .prof-home-card {
            border: 1px solid #dbeafe;
            border-radius: 14px;
            background: linear-gradient(180deg, #ffffff, #f8fbff);
            padding: 0.95rem 1rem 0.8rem;
            min-height: 138px;
            box-shadow: 0 8px 16px rgba(30, 64, 175, 0.08);
            margin-bottom: 0.55rem;
        }
        .prof-home-card h3 {
            margin: 0 0 0.25rem 0;
            color: #1e3a8a;
            font-size: 1.02rem;
        }
        .prof-home-card p {
            margin: 0;
            color: #475569;
            font-size: 0.9rem;
            line-height: 1.35rem;
        }
    </style>
    """,
    unsafe_allow_html=True,
)

col1, col2, col3 = st.columns(3, gap="large")

with col1:
    st.markdown(
        """
        <div class="prof-home-card">
          <h3>Manage Courses</h3>
          <p>Create classes, remove old sections, and keep your catalog current.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )
    if st.button("Open Courses", key="prof_home_courses", type="primary", use_container_width=True):
        st.switch_page("pages/11_Professor_Courses.py")

with col2:
    st.markdown(
        """
        <div class="prof-home-card">
          <h3>Student Roster</h3>
          <p>Review enrollments, check student activity, and remove students when needed.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )
    if st.button("Open Roster", key="prof_home_roster", type="primary", use_container_width=True):
        st.switch_page("pages/12_Professor_Roster.py")

with col3:
    st.markdown(
        """
        <div class="prof-home-card">
          <h3>Assignments</h3>
          <p>Create assignment plans and manage due dates and expected study benchmarks.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )
    if st.button("Open Assignments", key="prof_home_assignments", type="primary", use_container_width=True):
        st.switch_page("pages/13_Professor_Assignments.py")
