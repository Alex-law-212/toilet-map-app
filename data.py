import gspread
from google.oauth2.service_account import Credentials
from config import SERVICE_ACCOUNT_FILE, SPREADSHEET_NAME

def connect_sheet():
    scopes = [
        "https://www.googleapis.com/auth/spreadsheets",
        "https://www.googleapis.com/auth/drive"
    ]
    creds = Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=scopes)
    client = gspread.authorize(creds)
    return client.open(SPREADSHEET_NAME).sheet1

def get_all_locations():
    sheet = connect_sheet()
    return sheet.get_all_records()

def add_rating(name, score):
    sheet = connect_sheet()
    try:
        cell = sheet.find(name)
        row = cell.row
        current = sheet.cell(row, 5).value
        updated = current + f",{score}" if current else str(score)
        sheet.update_cell(row, 5, updated)
    except:
        raise ValueError("找不到該地點")

def calculate_average(ratings):
    if isinstance(ratings, int):
        scores = [ratings]
    elif isinstance(ratings, str):
        scores = [int(s) for s in ratings.split(",") if s.strip().isdigit()]
    else:
        scores = []

    return round(sum(scores) / len(scores), 2) if scores else 0

