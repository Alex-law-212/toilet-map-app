import streamlit as st
import json

SPREADSHEET_NAME = "pin_data"
ORS_API_KEY = st.secrets["ORS_API_KEY"]
GCP_CREDENTIALS = json.loads(st.secrets["GCP_CREDENTIALS"])
