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
st.markdown(
    """
    <style>
        .focusflow-hero {
            background: #1d4ed8;
            border: 1px solid #1e40af;
            border-radius: 16px;
            padding: 2rem 2.25rem;
            color: #eff6ff;
            margin-bottom: 1.25rem;
            box-shadow: 0 8px 20px rgba(29, 78, 216, 0.25);
        }
        .focusflow-hero h1 {
            margin: 0;
            font-size: 2.2rem;
            letter-spacing: 0.2px;
        }
        .focusflow-hero p {
            margin-top: 0.6rem;
            margin-bottom: 0;
            color: #dbeafe;
            font-size: 1.02rem;
        }
        .focusflow-card {
            background: linear-gradient(160deg, #f8fafc 0%, #f1f5f9 100%);
            border: 1px solid #e2e8f0;
            border-radius: 14px;
            padding: 1rem 1rem 0.6rem;
            margin-bottom: 0.6rem;
            min-height: 140px;
        }
        .focusflow-card h3 {
            margin: 0 0 0.3rem 0;
            color: #0f172a;
            font-size: 1.05rem;
        }
        .focusflow-card p {
            margin: 0;
            color: #475569;
            font-size: 0.92rem;
            line-height: 1.35rem;
        }
        .stButton button {
            border-radius: 10px;
            padding: 0.48rem 0.9rem;
            border: 0;
            font-weight: 600;
            box-shadow: 0 6px 14px rgba(37, 99, 235, 0.2);
        }
        .stButton button:hover {
            transform: translateY(-1px);
        }
    </style>
    """,
    unsafe_allow_html=True,
)

st.markdown(
    """
    <div class="focusflow-hero">
        <h1>FocusFlow</h1>
        <p>Select a role to enter your workspace and continue where you left off.</p>
    </div>
    """,
    unsafe_allow_html=True,
)

roles = [
    {
        "title": "Student",
        "icon": "🎓",
        "description": "Track assignments, visualize progress, and stay on top of daily tasks.",
        "button_label": "Continue as Student",
        "route": "pages/08_Student_Login.py",
    },
    {
        "title": "Professor",
        "icon": "📚",
        "description": "Manage courses, monitor student rosters, and publish assignments.",
        "button_label": "Continue as Professor",
        "route": "pages/09_Professor_Login.py",
    },
    {
        "title": "System Administrator",
        "icon": "🛠️",
        "description": "Oversee platform operations, records quality, and system maintenance.",
        "button_label": "Continue as System Administrator",
        "route": "pages/18_Admin_Login.py",
    },
    {
        "title": "Data Analyst",
        "icon": "📊",
        "description": "Explore engagement patterns, benchmark institutions, and export insights.",
        "button_label": "Continue as Data Analyst",
        "route": "pages/16_Analyst_Login.py",
    },
]

left_col, right_col = st.columns(2, gap="large")
for idx, role in enumerate(roles):
    col = left_col if idx % 2 == 0 else right_col
    with col:
        st.markdown(
            f"""
            <div class="focusflow-card">
                <h3>{role["icon"]} {role["title"]}</h3>
                <p>{role["description"]}</p>
            </div>
            """,
            unsafe_allow_html=True,
        )
        if st.button(role["button_label"], key=f"role_{idx}", type="primary", use_container_width=True):
            st.switch_page(role["route"])
