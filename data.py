import streamlit as st
import gspread
from google.oauth2.service_account import Credentials

from config import SERVICE_ACCOUNT_INFO, SPREADSHEET_NAME

# 建立與 Google Sheet 的連線
def connect_sheet():
    scopes = [
        "https://www.googleapis.com/auth/spreadsheets",
        "https://www.googleapis.com/auth/drive"
    ]
    creds = Credentials.from_service_account_info(SERVICE_ACCOUNT_INFO, scopes=scopes)
    client = gspread.authorize(creds)
    sheet = client.open(SPREADSHEET_NAME).sheet1
    return sheet

# 讀取所有地點資料（加上快取，避免每次重新抓）
@st.cache_data(ttl=600)  # 缓存时间：10分鐘，可自由调整
def get_all_locations():
    sheet = connect_sheet()
    return sheet.get_all_records()

# 新增評分：將新評分接在原本 ratings 欄位後面
def add_rating(name, score):
    sheet = connect_sheet()
    try:
        cell = sheet.find(name)
        row = cell.row
        current = sheet.cell(row, 5).value
        if current:
            updated = f"{current},{score}"
        else:
            updated = str(score)
        sheet.update_cell(row, 5, updated)
    except Exception as e:
        raise ValueError(f"找不到地點或寫入錯誤：{e}")

# 計算平均評分（僅納入 1~5 分、支援 float 格式）
    def calculate_average(ratings):
    try:
        # 轉成字串處理，不管來源是數字、空值、None 都能處理
        scores = [float(s) for s in str(ratings).split(",") if s.strip() and 1 <= float(s) <= 5]
        return round(sum(scores) / len(scores), 2) if scores else 0
    except:
        return 0
