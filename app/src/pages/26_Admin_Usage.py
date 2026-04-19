import logging
logger = logging.getLogger(__name__)

import streamlit as st
from modules.nav import SideBarLinks
from modules.api_client import api_get, show_api_error

st.set_page_config(page_title="System Usage", layout="wide")
SideBarLinks()

st.title("System-Wide Usage")
st.write("Monitor platform usage across institutions.")

users = []
try:
    users = api_get("/admin/users").get("users", [])
except Exception as exc:
    show_api_error(exc)

if not users:
    st.info("No usage data found.")
else:
    total_users = sum(int(row.get("user_count", 0) or 0) for row in users)

    m1 = st.columns(1)[0]
    with m1:
        st.metric("Total Users", total_users)

    st.subheader("Users by Institution")
    st.dataframe(users, use_container_width=True)