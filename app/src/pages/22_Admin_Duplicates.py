import logging
logger = logging.getLogger(__name__)

import streamlit as st
from modules.nav import SideBarLinks
from modules.api_client import api_get, api_delete, show_api_error

st.set_page_config(page_title="Duplicate Logs", layout="wide")
SideBarLinks()

st.title("Duplicate Activity Logs")
st.write("Review and delete duplicate activity log entries.")

duplicates = []
try:
    duplicates = api_get("/admin/logs/duplicates").get("duplicates", [])
except Exception as exc:
    show_api_error(exc)

if not duplicates:
    st.success("No duplicate logs found.")
else:
    for row in duplicates:
        log_id = row.get("log_id")
        st.write(
            f"**Log ID:** {log_id} | "
            f"User ID: {row.get('user_id')} | "
            f"Task ID: {row.get('task_id')} | "
            f"Category: {row.get('category')} | "
            f"Duration: {row.get('duration')} | "
            f"Logged At: {row.get('logged_at')}"
        )

        if st.button(f"Delete Duplicate Log {log_id}", key=f"delete_dup_{log_id}"):
            try:
                api_delete(f"/admin/logs/duplicates?log_id={log_id}")
                st.success(f"Deleted duplicate log {log_id}.")
                st.rerun()
            except Exception as exc:
                show_api_error(exc)