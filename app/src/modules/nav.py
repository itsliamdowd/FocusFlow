# Idea borrowed from https://github.com/fsmosca/sample-streamlit-authenticator

# This file has functions to add links to the left sidebar based on the user's role.

import streamlit as st


def apply_global_theme():
    """Apply shared visual theme across all app pages."""
    st.markdown(
        """
        <style>
            :root {
                --focusflow-heading-bg: #1e40af;
                --focusflow-heading-border: rgba(191, 219, 254, 0.42);
                --focusflow-heading-shadow: 0 10px 20px rgba(30, 64, 175, 0.22);
                --focusflow-heading-text: #eff6ff;
            }
            .stApp {
                background:
                    radial-gradient(circle at top right, rgba(59, 130, 246, 0.12), transparent 42%),
                    linear-gradient(180deg, #f8fbff 0%, #eef4ff 100%);
            }
            [data-testid="stHeader"] {
                background: transparent;
            }
            [data-testid="stSidebar"] {
                background: linear-gradient(180deg, #e9f1ff 0%, #dbeafe 100%);
                border-right: 1px solid #bfdbfe;
            }
            [data-testid="stSidebar"] * {
                color: #1e3a8a;
            }
            [data-testid="stSidebar"] button[kind="secondary"] {
                border-radius: 10px;
                border: 1px solid #93c5fd;
                background: #ffffff;
            }
            [data-testid="stSidebar"] button[kind="secondary"]:hover {
                border-color: #60a5fa;
                background: #eff6ff;
            }
            .stButton > button {
                border-radius: 10px;
            }
            div[data-testid="stForm"] {
                border: 1px solid #bfdbfe;
                border-radius: 12px;
                background: linear-gradient(180deg, #ffffff, #f8fbff);
            }
            div[data-testid="stMetric"] {
                background: #ffffff;
                border: 1px solid #dbeafe;
                border-radius: 12px;
                padding: 0.5rem 0.8rem;
            }
            /* Theme only native Streamlit page titles (st.title), not custom HTML hero headings. */
            .stApp [data-testid="stHeadingWithActionElements"] h1 {
                background: var(--focusflow-heading-bg);
                border: 1px solid var(--focusflow-heading-border);
                border-radius: 16px;
                padding: 0.95rem 1.15rem;
                color: var(--focusflow-heading-text);
                box-shadow: var(--focusflow-heading-shadow);
                margin-bottom: 0.9rem;
            }
            /* Force all hero heading containers to use the exact same heading color style. */
            .stMarkdown .focusflow-hero,
            .stMarkdown .student-hero,
            .stMarkdown .task-hero,
            .stMarkdown .timer-hero {
                background: var(--focusflow-heading-bg) !important;
                border: 1px solid var(--focusflow-heading-border) !important;
                box-shadow: var(--focusflow-heading-shadow) !important;
                color: var(--focusflow-heading-text) !important;
            }
            /* If a page uses its own hero container, keep only the outer hero box. */
            .stMarkdown .focusflow-hero h1,
            .stMarkdown .student-hero h1,
            .stMarkdown .task-hero h1,
            .stMarkdown .timer-hero h1 {
                background: transparent;
                border: 0;
                border-radius: 0;
                box-shadow: none;
                padding: 0;
                margin-bottom: 0;
                color: inherit;
            }
            .stApp .block-container h2 {
                color: #1e3a8a;
            }
        </style>
        """,
        unsafe_allow_html=True,
    )

# ---- General ----------------------------------------------------------------

def home_nav():
    st.sidebar.page_link("Home.py", label="Home", icon="🏠")


def about_page_nav():
    st.sidebar.page_link("pages/30_About.py", label="About", icon="🧠")


# ---- Role: Student ------------------------------------------------

def student_home_nav():
    st.sidebar.page_link(
        "pages/00_Student_Home.py", label="Student Home", icon="📋"
    )


def tasks_viz_nav():
    st.sidebar.page_link(
        "pages/01_Tasks_Viz.py", label="Tasks Visualization", icon="📋"
    )

def timer_nav():
    st.sidebar.page_link(
        "pages/02_Timer.py", label = "Timer", icon = "⏱️"
    )

def student_analytics_nav():
    st.sidebar.page_link(
        "pages/03_student_analytics.py", label = "Analytics", icon = "📈"
    )

# ---- Role: Professor -----------------------------------------------------

def professor_home_nav():
    st.sidebar.page_link(
        "pages/10_Professor_Home.py", label="Professor Home", icon="🏠"
    )

def professor_courses_nav():
    st.sidebar.page_link("pages/11_Professor_Courses.py", label="My Courses", icon="📚")


def professor_roster_nav():
    st.sidebar.page_link("pages/12_Professor_Roster.py", label="Student Roster", icon="👥")


def professor_assignments_nav():
    st.sidebar.page_link("pages/13_Professor_Assignments.py", label="Assignments", icon="📝")


# ---- Role: Data Analyst ----------------------------------------------------

def data_analyst_home_nav():
    st.sidebar.page_link("pages/17_Data_Analyst_Home.py", label="Data Analyst Home", icon="🖥️")

def data_analyst_correlations_nav():
    st.sidebar.page_link("pages/31_Analyst_Correlations.py", label = "Correlations")

def data_analyst_trends_nav():
    st.sidebar.page_link("pages/32_Analyst_Trend_Flags.py", label = "Flag Trends")

def data_analyst_filtering_nav():
    st.sidebar.page_link("pages/33_Analyst_Filtering.py", label = "Filter Student Data")

def data_analyst_breakdown_nav():
    st.sidebar.page_link("pages/34_Analyst_Category_Breakdown.py", label = "Category Breakdown")

def data_analyst_sharing_nav():
    st.sidebar.page_link("pages/35_Analyst_Institution_Sharing.py", label = "Institution Sharing")

def data_analyst_export_nav():
    st.sidebar.page_link("pages/36_Analyst_Export.py", label = "Export Data")


# ---- Role: System Administrator ---------------------------------------------

def admin_home_nav():
    st.sidebar.page_link("pages/20_Admin_Home.py", label="System Admin", icon="🖥️")


def admin_dupes_nav():
    st.sidebar.page_link("pages/22_Admin_Duplicates.py", label = "Duplicates")

def admin_records_nav():
    st.sidebar.page_link("pages/23_Admin_Records.py", label = "Incorrect Records")

def admin_usage_nav():
    st.sidebar.page_link("pages/26_Admin_Usage.py", label="System Usage")

def admin_categories_nav():
    st.sidebar.page_link("pages/24_Admin_Categories.py", label="Update Categories")

def admin_archive_nav():
    st.sidebar.page_link("pages/27_Admin_Archive.py", label="Archive")

# ---- Sidebar assembly -------------------------------------------------------

def SideBarLinks(show_home=False):
    """
    Renders sidebar navigation links based on the logged-in user's role.
    The role is stored in st.session_state when the user logs in on Home.py.
    """

    # Apply shared page-level visual style before rendering content.
    apply_global_theme()

    # Logo appears at the top of the sidebar on every page
    st.sidebar.image("assets/logo.png", width=150)

    # If no one is logged in, send them to the Home (login) page
    if "authenticated" not in st.session_state:
        st.session_state.authenticated = False
        st.switch_page("Home.py")

    if show_home:
        home_nav()

    if st.session_state["authenticated"]:

        if st.session_state["role"] == "student":
            student_home_nav()
            tasks_viz_nav()
            timer_nav()
            student_analytics_nav()

        if st.session_state["role"] == "professor":
            professor_home_nav()
            professor_courses_nav()
            professor_roster_nav()
            professor_assignments_nav()

        if st.session_state["role"] == "data analyst":
            data_analyst_home_nav()
            data_analyst_correlations_nav()
            data_analyst_trends_nav()
            data_analyst_filtering_nav()
            data_analyst_breakdown_nav()
            data_analyst_sharing_nav()
            data_analyst_export_nav()


        if st.session_state["role"] == "system admin":
            admin_home_nav()
            admin_dupes_nav()
            admin_records_nav()
            admin_usage_nav()
            admin_categories_nav()
            admin_archive_nav()

    # About link appears at the bottom for all roles
    about_page_nav()

    if st.session_state["authenticated"]:
        if st.sidebar.button("Logout"):
            for key in ["role", "authenticated", "user_id", "institution_id", "first_name"]:
                if key in st.session_state:
                    del st.session_state[key]
            st.switch_page("Home.py")
