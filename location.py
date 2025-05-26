import streamlit as st
from streamlit_geolocation import streamlit_geolocation
import folium
from streamlit_folium import st_folium

def get_user_location():
    # 嘗試使用 GPS 定位
    st.markdown("### 📡 嘗試從瀏覽器定位（需允許存取）")
    location = streamlit_geolocation()
    if location and location.get("latitude") and location.get("longitude"):
        lat = location["latitude"]
        lng = location["longitude"]
        st.success(f"✅ GPS 取得成功：({lat}, {lng})")
        return (lat, lng)

    # 若 GPS 失敗，提供互動地圖點選
    st.markdown("---")
    st.markdown("### 🗺️ 點擊地圖來選擇位置（替代 GPS）")

    default_center = [25.0330, 121.5654]  # 台北為預設中心
    m = folium.Map(location=default_center, zoom_start=13)
    st.markdown("👇 請點擊地圖標記你的位置")
    output = st_folium(m, height=500, width=700)

    if output and output.get("last_clicked"):
        lat = output["last_clicked"]["lat"]
        lng = output["last_clicked"]["lng"]
        st.success(f"✅ 地圖選擇位置：({lat:.6f}, {lng:.6f})")
        return (lat, lng)

    # 都沒有定位成功
    st.info("📭 尚未定位，請點擊地圖或允許定位權限")
    return None
