import logging
import streamlit as st
import pandas as pd

from modules.nav import SideBarLinks
from modules.api_client import api_get, api_put, show_api_error

logger = logging.getLogger(__name__)

st.set_page_config(layout="wide")
SideBarLinks()

st.title("Flag Concerning Trends")
st.write("Review activity logs and flag suspicious records as anomalous.")

st.subheader("Filters")

institutions = []
try:
    institutions = api_get("/analyst/institutions").get("institutions", [])
except Exception as exc:
    show_api_error(exc)

institution_options = [("All Institutions", None)]
for row in institutions:
    institution_options.append((row.get("name", "Unknown"), row.get("institution_id")))

col1, col2, col3 = st.columns(3)

with col1:
    selected_label = st.selectbox(
        "Institution",
        options=[label for label, _ in institution_options]
    )

selected_institution_id = None
for label, value in institution_options:
    if label == selected_label:
        selected_institution_id = value
        break

with col2:
    major_filter = st.text_input("Major")

with col3:
    year_filter = st.selectbox("Year", ["All", 1, 2, 3, 4, 5])

params = {}
if selected_institution_id:
    params["institution_id"] = selected_institution_id
if major_filter.strip():
    params["major"] = major_filter.strip()
if year_filter != "All":
    params["year"] = year_filter

activity = []
try:
    activity = api_get("/analyst/activity", params=params).get("activity", [])
except Exception as exc:
    show_api_error(exc)

if not activity:
    st.info("No activity logs found for the selected filters.")
else:
    df = pd.DataFrame(activity)

    if "duration" in df.columns:
        df["duration"] = pd.to_numeric(df["duration"], errors="coerce").fillna(0)

    st.subheader("Quick Trend Checks")

    c1, c2, c3 = st.columns(3)
    with c1:
        high_duration_count = int((df["duration"] > 300).sum()) if "duration" in df.columns else 0
        st.metric("Logs Over 300 Minutes", high_duration_count)

    with c2:
        archived_count = int((df["archived"] == 1).sum()) if "archived" in df.columns else 0
        st.metric("Already Archived", archived_count)

    with c3:
        st.metric("Logs in View", len(df))

    st.subheader("Potentially Concerning Logs")
    st.write("Suggestion: long sessions, unusual entries, or suspicious records can be flagged below.")

    suspicious_logs_found = False
    for row in activity:
        log_id = row.get("log_id")
        duration = row.get("duration")
        try:
            duration_num = float(duration)
        except (TypeError, ValueError):
            continue

        if not (duration_num > 300 or duration_num <= 0):
            continue

        suspicious_logs_found = True
        category = row.get("category")
        user_name = f"{row.get('first_name', '')} {row.get('last_name', '')}".strip()
        major = row.get("major", "—")
        year = row.get("year", "—")
        logged_at = row.get("logged_at", "—")
        archived = row.get("archived", False)

        with st.expander(f"Log {log_id} | {user_name} | {category} | {duration} min"):
            st.write(f"**User:** {user_name}")
            st.write(f"**Major:** {major}")
            st.write(f"**Year:** {year}")
            st.write(f"**Logged At:** {logged_at}")
            st.write(f"**Archived:** {archived}")

            suspicious = False
            reasons = []

            if duration_num > 300:
                suspicious = True
                reasons.append("Very long duration")
            if duration_num <= 0:
                suspicious = True
                reasons.append("Non-positive duration")

            if reasons:
                st.warning("Possible issue: " + ", ".join(reasons))
            else:
                st.info("No obvious automatic flag found, but you can still mark it if needed.")

            if archived:
                st.success("This log is already archived / flagged.")
            else:
                if st.button("Flag as Anomalous", key=f"flag_{log_id}"):
                    try:
                        api_put(f"/analyst/activity/{log_id}", {"is_anomalous": True})
                        st.success(f"Log {log_id} flagged successfully.")
                        st.rerun()
                    except Exception as exc:
                        show_api_error(exc)

    if not suspicious_logs_found:
        st.info("No suspicious logs matched the current rules.")

    st.subheader("Activity Table")
    display_cols = [
        col for col in [
            "log_id",
            "user_id",
            "first_name",
            "last_name",
            "major",
            "year",
            "category",
            "duration",
            "logged_at",
            "archived"
        ] if col in df.columns
    ]
    st.dataframe(df[display_cols], use_container_width=True)
