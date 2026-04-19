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
st.write('Who would you like to login as')

# For each of the user personas for which we are implementing
# functionality, we put a button on the screen that the user
# can click to MIMIC logging in as that mock user.

if st.button("Act as Maya, a Student.",
             type='primary',
             use_container_width=True):
    # when user clicks the button, they are now considered authenticated
    st.session_state['authenticated'] = True
    # we set the role of the current user
    st.session_state['role'] = 'student'
    # we add the first name of the user (so it can be displayed on
    # subsequent pages).
    st.session_state['first_name'] = 'Maya'
    st.session_state['user_id'] = 1
    st.session_state['institution_id'] = 1
    # finally, we ask streamlit to switch to another page, in this case, the
    # landing page for this particular user type
    logger.info("Logging in as Student Persona")
    st.switch_page('pages/00_Student_Home.py')

if st.button('Act as Dr. Smith a Professor', type='primary', use_container_width=True):
    st.session_state['authenticated'] = True
    st.session_state['role'] = 'professor'
    st.session_state['first_name'] = 'Dr. Smith'
    st.switch_page('pages/09_Professor_Login.py')

if st.button('Act as Jimmy, a System Administrator',
             type='primary',
             use_container_width=True):
    st.session_state['authenticated'] = True
    st.session_state['role'] = 'system admin'
    st.session_state['first_name'] = 'Jimmy'
    st.switch_page('pages/20_Admin_Home.py')

if st.button('Act as James, a Data Analyst.',
             type='primary',
             use_container_width=True):
    st.session_state['authenticated'] = True
    st.session_state['role'] = 'data analyst'
    st.session_state['first_name'] = 'James'
    st.switch_page('pages/17_Data_Analyst_Home.py')
