import requests
import streamlit as st

def get_user_location_by_ip():
    try:
        res = requests.get("https://ipinfo.io/json")
        data = res.json()
        st.write("🌐 IP 定位資料：", data)
        loc = data["loc"]  # 例如："25.0173,121.5398"
        lat, lng = map(float, loc.split(","))
        return (lat, lng)
    except Exception as e:
        st.error(f"❌ IP 定位失敗：{e}")
        return None

