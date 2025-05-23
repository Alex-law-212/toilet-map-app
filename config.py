import streamlit as st

# 读取 Google Sheet 与 Service Account 相关信息
SERVICE_ACCOUNT_INFO = st.secrets["google"]
SPREADSHEET_NAME = st.secrets["google"]["spreadsheet_name"]

# 读取 OpenRouteService API 金钥
ORS_API_KEY = st.secrets["ors"]["api_key"]
