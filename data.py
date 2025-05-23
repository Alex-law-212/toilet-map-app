import gspread
import json
import streamlit as st
from google.oauth2.service_account import Credentials
from config import SPREADSHEET_NAME

def connect_sheet():
    scopes = [
        "https://www.googleapis.com/auth/spreadsheets",
        "https://www.googleapis.com/auth/drive"
    ]
    creds_dict = json.loads(st.secrets["gcp_service_account"])  # ← 使用 secrets 中的 JSON 字串
    creds = Credentials.from_service_account_info(creds_dict, scopes=scopes)
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
