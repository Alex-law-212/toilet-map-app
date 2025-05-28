import gspread
from google.oauth2.service_account import Credentials

from config import SERVICE_ACCOUNT_INFO, SPREADSHEET_NAME

# === 建立連線 ===
def connect_sheet():
    scopes = [
        "https://www.googleapis.com/auth/spreadsheets",
        "https://www.googleapis.com/auth/drive",
    ]
    creds = Credentials.from_service_account_info(SERVICE_ACCOUNT_INFO, scopes=scopes)
    client = gspread.authorize(creds)
    sheet = client.open(SPREADSHEET_NAME).sheet1
    return sheet

# === 新增留言 ===
def add_comment(name, comment):
    sheet = connect_sheet()
    try:
        cell = sheet.find(name)
        row = cell.row
        current = sheet.cell(row, 6).value  # 第 6 欄是 comments 欄位
        updated = f"{current} | {comment}" if current else comment
        sheet.update_cell(row, 6, updated)
    except Exception as e:
        raise ValueError(f"寫入留言失敗：{e}")

# === 拆分留言字串為清單 ===
def get_comments(comment_str):
    if not comment_str:
        return []
    return [c.strip() for c in comment_str.split("|") if c.strip()]
