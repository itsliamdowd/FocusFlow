import logging
logger = logging.getLogger(__name__)

import pandas as pd
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
    df = pd.DataFrame(duplicates)
    if "log_id" not in df.columns:
        st.error("Duplicate logs response is missing log_id.")
    else:
        df = df.copy()
        df.insert(0, "select", False)
        st.caption("Select one or more duplicate logs, then delete them.")
        edited_df = st.data_editor(
            df,
            hide_index=True,
            use_container_width=True,
            disabled=[col for col in df.columns if col != "select"],
            column_config={
                "select": st.column_config.CheckboxColumn("Select")
            },
            key="duplicate_logs_table",
        )

        selected_log_ids = edited_df.loc[edited_df["select"], "log_id"].tolist()
        if st.button("Delete Selected Duplicate Logs", type="primary", disabled=not selected_log_ids):
            deleted_count = 0
            for log_id in selected_log_ids:
                try:
                    api_delete(f"/admin/logs/duplicates?log_id={log_id}")
                    deleted_count += 1
                except Exception as exc:
                    show_api_error(exc)
                    break
            if deleted_count:
                st.success(f"Deleted {deleted_count} duplicate log(s).")
                st.rerun()