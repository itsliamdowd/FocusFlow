##################################################
# This is the main/entry-point file for the
# sample application for your project
##################################################

# Set up basic logging infrastructure
import logging
logging.basicConfig(format='%(filename)s:%(lineno)s:%(levelname)s -- %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# import the main streamlit library as well
# as SideBarLinks function from src/modules folder
import streamlit as st
from modules.nav import SideBarLinks

# streamlit supports regular and wide layout (how the controls
# are organized/displayed on the screen).
st.set_page_config(layout='wide')

# If a user is at this page, assume unauthenticated by default.
st.session_state.setdefault('authenticated', False)

# Use the SideBarLinks function from src/modules/nav.py to control
# the links displayed on the left-side panel.
# IMPORTANT: ensure src/.streamlit/config.toml sets
# showSidebarNavigation = false in the [client] section
SideBarLinks(show_home=True)

# ***************************************************
#    The major content of this page
# ***************************************************

logger.info("Loading the Home page of the app")
st.title('FocusFlow')
st.write('Who would you like to act as')

# For each of the user types for which we are implementing
# functionality, we put a button on the screen that the user
# can click to go to the login page for that type of user

if st.button("Act as Student", type='primary', use_container_width=True):
    st.switch_page('pages/08_Student_Login.py')

if st.button('Act as Professor', type='primary', use_container_width=True):
    st.switch_page('pages/09_Professor_Login.py')

if st.button('Act as System Administrator', type='primary', use_container_width=True):
    st.switch_page('pages/18_Admin_Login.py')

if st.button('Act as Data Analyst', type='primary', use_container_width=True):
    st.switch_page('pages/16_Analyst_Login.py')
