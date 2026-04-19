import logging
logger = logging.getLogger(__name__)

import streamlit as st
from modules.nav import SideBarLinks

st.set_page_config(layout='wide')

SideBarLinks()

st.title('Admin Console')
st.write('Select a task to get started.')

if st.button('Remove Duplicate Activity Logs',
             type='primary',
             use_container_width=True):
    st.switch_page('pages/22_Admin_Duplicates.py')

if st.button('Update Incorrect Records',
             type='primary',
             use_container_width=True):
    st.switch_page('pages/23_Admin_Records.py')

if st.button('Manage Categories',
             type='primary',
             use_container_width=True):
    st.switch_page('pages/24_Admin_Categories.py')

if st.button('Monitor System-Wide Usage',
             type='primary',
             use_container_width=True):
    st.switch_page('pages/26_Admin_Usage.py')

if st.button('Archive Old Data',
             type='primary',
             use_container_width=True):
    st.switch_page('pages/27_Admin_Archive.py')
