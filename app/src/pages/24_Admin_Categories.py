import logging
logger = logging.getLogger(__name__)

import streamlit as st
from modules.nav import SideBarLinks
from modules.api_client import api_get, api_delete, show_api_error

st.set_page_config(page_title="Categories", layout="wide")
SideBarLinks()

st.title("Activity Categories")
st.write("View categories in use and remove outdated categories from the logs.")

categories = []
try:
    categories = api_get("/admin/categories").get("categories", [])
except Exception as exc:
    show_api_error(exc)

if not categories:
    st.info("No categories found.")
else:
    st.subheader("Categories Currently In Use")
    for category in categories:
        st.write(f"- {category}")

st.divider()

if categories:
    category_to_remove = st.selectbox("Choose category to remove", categories)
    st.warning("Warning: this will permanently delete all activity logs under the selected category.")
    if st.button("Delete Category Logs", type="primary"):
        try:
            api_delete(f"/admin/categories?category={category_to_remove}")
            st.success(f"Deleted logs under category '{category_to_remove}'.")
            st.rerun()
        except Exception as exc:
            show_api_error(exc)