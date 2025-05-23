import streamlit as st

# 讀取 Google Sheet 名稱
SPREADSHEET_NAME = "pin_data"

# 讀取 OpenRouteService 的 API 金鑰（從 secrets 裡）
ORS_API_KEY = st.secrets["ORS_API_KEY"]

# 讀取 Google 憑證（從 secrets 裡）
GCP_CREDENTIALS = dict(st.secrets["gcp_service_account"])
