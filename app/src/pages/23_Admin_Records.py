import logging
logger = logging.getLogger(__name__)
import streamlit as st
from modules.nav import SideBarLinks
from modules.api_client import api_get, api_put, show_api_error

st.set_page_config(page_title="Incorrect Records", layout="wide")
SideBarLinks()

st.title("Incorrect Activity Records")
st.write("Review logs and update incorrect duration or category values.")

if "found_log" not in st.session_state:
    st.session_state.found_log = None

log_id_input = st.number_input("Log ID", min_value=1, step=1, value=1)

if st.button("Find Log", type="primary"):
    try:
        payload = api_get(f"/admin/logs/{int(log_id_input)}")
        if isinstance(payload, dict):
            row = payload.get("log", payload)
            if isinstance(row, dict) and row.get("log_id") is not None:
                st.session_state.found_log = row
            else:
                st.session_state.found_log = None
        else:
            st.session_state.found_log = None
    except Exception as exc:
        st.session_state.found_log = None
        show_api_error(exc)

row = st.session_state.found_log
if not row:
    st.info("Enter a log ID and click Find Log to edit a specific record.")
else:
    log_id = row.get("log_id")

    current_category = row.get("category", "school")
    options = ["school", "work", "extracurricular", "personal"]
    default_index = options.index(current_category) if current_category in options else 0

    with st.expander(f"Log {log_id} | User {row.get('user_id')} | {current_category}", expanded=True):
        st.write(f"Task ID: {row.get('task_id')}")
        st.write(f"Logged At: {row.get('logged_at')}")
        st.write(f"Archived: {row.get('archived')}")

        new_duration = st.number_input(
            "New Duration",
            min_value=0,
            value=int(row.get("duration") or 0),
            key=f"duration_{log_id}",
        )

        new_category = st.selectbox(
            "New Category",
            options,
            index=default_index,
            key=f"category_{log_id}",
        )

        if st.button("Save Record Update", key=f"save_record_{log_id}"):
            try:
                api_put(
                    f"/admin/logs/{log_id}",
                    {
                        "duration": int(new_duration),
                        "category": new_category,
                    },
                )
                st.success(f"Updated log {log_id}.")
                st.rerun()
            except Exception as exc:
                show_api_error(exc)