import streamlit as st
from streamlit_geolocation import streamlit_geolocation

def get_user_location():
    try:
        location = streamlit_geolocation()
        st.write("🧭 取得的位置資料：", location)  # 除錯用，可移除

        if location and location.get("latitude") is not None and location.get("longitude") is not None:
            return (location["latitude"], location["longitude"])
        else:
            st.warning("⚠️ 無法取得定位，請確認是否授權定位權限")
            return None
    except Exception as e:
        st.error(f"❌ 發生錯誤：{e}")
        return None
