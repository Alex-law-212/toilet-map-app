import streamlit as st
import gspread
from google.oauth2.service_account import Credentials

from config import GCP_CREDENTIALS, SPREADSHEET_NAME

def connect_sheet():
    scopes = [
        "https://www.googleapis.com/auth/spreadsheets",
        "https://www.googleapis.com/auth/drive"
    ]
    creds = Credentials.from_service_account_info(GCP_CREDENTIALS, scopes=scopes)
    client = gspread.authorize(creds)
    sheet = client.open(SPREADSHEET_NAME).sheet1
    return sheet

def get_all_locations():
    sheet = connect_sheet()
    return sheet.get_all_records()

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

def calculate_average(ratings):
    if isinstance(ratings, int):
        scores = [ratings]
    elif isinstance(ratings, str):
        scores = [int(s) for s in ratings.split(",") if s.strip().isdigit()]
    else:
        scores = []
    return round(sum(scores) / len(scores), 2) if scores else 0
