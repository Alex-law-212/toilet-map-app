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
        sheet.update_cell(row, 5, updated)
    except Exception as e:
        raise ValueError(f"找不到地點或寫入錯誤：{e}")

# 計算平均評分（僅納入 1~5 分、支援 float 格式）
def calculate_average(rating_str):
    import json
    try:
        ratings = json.loads(rating_str)
    except:
        try:
            ratings = [r.strip() for r in rating_str.split(",") if r.strip()]
        except:
            ratings = []

    if not ratings:
        return "-"
    try:
        scores = [int(r) for r in ratings if r.isdigit()]
        return round(sum(scores) / len(scores), 1) if scores else "-"
    except:
        return "-"
