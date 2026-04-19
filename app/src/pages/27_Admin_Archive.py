import logging
logger = logging.getLogger(__name__)

import streamlit as st
from modules.nav import SideBarLinks
from modules.api_client import api_get, api_post, show_api_error

st.set_page_config(page_title="Archive Logs", layout="wide")
SideBarLinks()

st.title("Archive Old Logs")
st.write("View archived logs and archive logs older than a cutoff date.")

archived = []
try:
    archived = api_get("/admin/logs/archive").get("archived", [])
except Exception as exc:
    show_api_error(exc)

st.subheader("Archive Logs Older Than a Cutoff Date")
cutoff_date = st.date_input("Cutoff Date")

if st.button("Archive Logs", type="primary"):
    try:
        api_post(
            "/admin/logs/archive",
            {"cutoff_date": cutoff_date.strftime("%Y-%m-%d")},
        )
        st.success("Archive job completed.")
        st.rerun()
    except Exception as exc:
        show_api_error(exc)

st.divider()

st.subheader("Archived Logs")
if not archived:
    st.info("No archived logs found.")
else:
    st.dataframe(archived, use_container_width=True)