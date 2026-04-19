import logging
import streamlit as st
import pandas as pd

from modules.nav import SideBarLinks
from modules.api_client import api_get, show_api_error

logger = logging.getLogger(__name__)

st.set_page_config(layout="wide")
SideBarLinks()

st.title("Study Time vs Productivity Correlations")
st.write("Analyze how total study time aligns with average productivity scores.")

institution_id = st.session_state.get("institution_id")

st.subheader("Filters")

institutions = []
selected_institution_id = None

try:
    institutions = api_get("/analyst/institutions").get("institutions", [])
except Exception as exc:
    show_api_error(exc)

institution_options = [("All Institutions", None)]
for row in institutions:
    institution_options.append((row.get("name", "Unknown"), row.get("institution_id")))

selected_label = st.selectbox(
    "Institution",
    options=[label for label, _ in institution_options]
)

for label, value in institution_options:
    if label == selected_label:
        selected_institution_id = value
        break

params = {}
if selected_institution_id:
    params["institution_id"] = selected_institution_id

correlations = []
try:
    correlations = api_get("/analyst/correlations", params=params).get("correlations", [])
except Exception as exc:
    show_api_error(exc)

if not correlations:
    st.info("No correlation data found.")
else:
    df = pd.DataFrame(correlations)

    # Normalize study-time naming in case backend aliases change.
    if "total_minutes" not in df.columns:
        for alt_col in ["study_minutes", "total_duration", "duration"]:
            if alt_col in df.columns:
                df["total_minutes"] = df[alt_col]
                break

    if "total_minutes" in df.columns:
        df["total_minutes"] = pd.to_numeric(df["total_minutes"], errors="coerce").fillna(0)
        df["study_hours"] = (df["total_minutes"] / 60.0).round(2)

    if "avg_productivity" in df.columns:
        df["avg_productivity"] = pd.to_numeric(df["avg_productivity"], errors="coerce").fillna(0)

    m1, m2, m3 = st.columns(3)
    with m1:
        st.metric("Users in View", len(df))
    with m2:
        avg_minutes = round(df["total_minutes"].mean(), 2) if "total_minutes" in df.columns else 0
        st.metric("Avg Total Minutes", avg_minutes)
    with m3:
        avg_score = round(df["avg_productivity"].mean(), 2) if "avg_productivity" in df.columns else 0
        st.metric("Avg Productivity", avg_score)

    st.subheader("Scatter Plot")
    if "total_minutes" in df.columns and "avg_productivity" in df.columns:
        scatter_df = df.rename(
            columns={
                "total_minutes": "Total Minutes",
                "avg_productivity": "Avg Productivity"
            }
        )
        st.scatter_chart(
            scatter_df,
            x="Total Minutes",
            y="Avg Productivity"
        )
    else:
        st.info("The backend did not return the expected columns for plotting.")

    st.subheader("Correlation Table")
    display_cols = [
        col for col in [
            "user_id",
            "first_name",
            "last_name",
            "total_minutes",
            "study_hours",
            "avg_productivity"
        ] if col in df.columns
    ]
    st.dataframe(df[display_cols], use_container_width=True)

    if "total_minutes" in df.columns and "avg_productivity" in df.columns and len(df) >= 2:
        corr_value = df["total_minutes"].corr(df["avg_productivity"])
        if pd.notna(corr_value):
            st.subheader("Pearson Correlation")
            st.write(f"Correlation between total minutes and average productivity: **{corr_value:.3f}**")
        else:
            st.write("Not enough valid numeric data to compute a correlation.")
