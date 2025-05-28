import gspread
import streamlit as st
from google.oauth2.service_account import Credentials

# 從 Streamlit secrets 讀取設定
SERVICE_ACCOUNT_INFO = st.secrets["google"]
SPREADSHEET_NAME = st.secrets["google"]["spreadsheet_name"]

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

# 新增留言：接在原有留言後
def add_comment(name, comment):
    sheet = connect_sheet()
    try:
        cell = sheet.find(name)
        row = cell.row
        current = sheet.cell(row, 6).value  # 第 6 欄是 comments
        updated = f"{current} | {comment}" if current else comment
        sheet.update_cell(row, 6, updated)
    except Exception as e:
        raise ValueError(f"❌ 寫入留言失敗：{e}")

# 將留言字串拆分為清單
def get_comments(comment_str):
    if not comment_str:
        return []
    return [c.strip() for c in comment_str.split("|") if c.strip()]
