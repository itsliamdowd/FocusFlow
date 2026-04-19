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
            background: radial-gradient(circle at top right, #3b82f6 0%, #1d4ed8 45%, #1e3a8a 100%);
            border: 1px solid rgba(191, 219, 254, 0.35);
            border-radius: 18px;
            padding: 2rem 2.25rem 1.5rem;
            color: #eff6ff;
            margin-bottom: 1.25rem;
            box-shadow: 0 14px 28px rgba(30, 58, 138, 0.35);
        }
        .focusflow-hero h1 {
            margin: 0;
            font-size: 2.2rem;
            letter-spacing: 0.2px;
        }
        .focusflow-hero p {
            margin-top: 0.6rem;
            margin-bottom: 0.9rem;
            color: #dbeafe;
            font-size: 1.02rem;
        }
        .focusflow-chip-wrap {
            display: flex;
            gap: 0.45rem;
            flex-wrap: wrap;
        }
        .focusflow-chip {
            display: inline-block;
            border-radius: 999px;
            padding: 0.2rem 0.6rem;
            border: 1px solid rgba(219, 234, 254, 0.5);
            background: rgba(30, 64, 175, 0.38);
            color: #dbeafe;
            font-size: 0.78rem;
            font-weight: 600;
        }
        .focusflow-section-title {
            margin: 0.35rem 0 0.75rem 0;
            font-size: 1rem;
            color: #1e3a8a;
            font-weight: 700;
            letter-spacing: 0.02em;
            text-transform: uppercase;
        }
        .focusflow-card {
            background: linear-gradient(160deg, #ffffff 0%, #f8fafc 100%);
            border: 1px solid #dbeafe;
            border-radius: 14px;
            padding: 1rem 1rem 0.8rem;
            margin-bottom: 0.5rem;
            min-height: 140px;
            box-shadow: 0 10px 18px rgba(15, 23, 42, 0.06);
            transition: transform 0.18s ease, box-shadow 0.18s ease, border-color 0.18s ease;
        }
        .focusflow-card:hover {
            transform: translateY(-2px);
            box-shadow: 0 14px 24px rgba(30, 64, 175, 0.14);
            border-color: #93c5fd;
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
            padding: 0.55rem 0.9rem;
            border: 0;
            font-weight: 700;
            box-shadow: 0 8px 16px rgba(37, 99, 235, 0.22);
            background: #2563eb;
        }
        .stButton button:hover {
            transform: translateY(-1px);
            background: #1d4ed8;
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
        <div class="focusflow-chip-wrap">
            <span class="focusflow-chip">Task Planning</span>
            <span class="focusflow-chip">Role Dashboards</span>
            <span class="focusflow-chip">Analytics Insights</span>
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)
st.markdown('<div class="focusflow-section-title">Choose Your Workspace</div>', unsafe_allow_html=True)

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
