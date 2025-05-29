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
        st.write(f"將寫入的評分字串: {updated}")
        sheet.update_cell(row, 5, updated)
    except Exception as e:
        raise ValueError(f"找不到地點或寫入錯誤：{e}")
#计算平均评分
def calculate_average(rating_str):
    if not rating_str:
        return "-"

    try:
        digits = [int(ch) for ch in str(rating_str) if ch in "12345"]
        return round(sum(digits) / len(digits), 1) if digits else "-"
    except:
        return "-"
#將評分字串拆解為要显示的模式
def split_ratings_readable(rating_str):
    if not rating_str:
        return "-"
    clean = str(rating_str).replace("［", "").replace("］", "").replace("[", "").replace("]", "")
    clean = clean.replace("，", ",")
    parts = clean.split(",")
    digits = [r.strip() for r in parts if r.strip().isdigit()]
    return "、".join(digits) if digits else "-"
