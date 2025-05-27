import streamlit as st
import folium
from streamlit_folium import st_folium

from data import get_all_locations, add_rating, calculate_average
from geo import find_nearest
from route import get_route
from location import get_user_location

# === 初次載入資料 ===
if "location_data" not in st.session_state:
    st.session_state["location_data"] = get_all_locations()

# === 頁面設定 ===
st.set_page_config(page_title="📍 地標互動地圖系統", layout="wide")
st.title("📍 地標互動地圖 + 評分系統")

# === 類別選單 ===
category_ui = st.radio("📂 顯示類型", ["全部", "餐廳", "廁所"])
category_map = {"全部": None, "餐廳": "restaurant", "廁所": "toilet"}
category = category_map[category_ui]

# === 載入資料 ===
data = st.session_state["location_data"]
if category is None:
    filtered = data
else:
    filtered = [p for p in data if p.get("type", "").strip().lower() == category]

# === 初始化 session_state ===
if "user_pos" not in st.session_state:
    st.session_state["user_pos"] = None
if "route_coords" not in st.session_state:
    st.session_state["route_coords"] = []

profile = "foot-walking"

# === 取得定位區塊 ===
with st.expander("📍 定位選項", expanded=True):
    if st.button("📍 嘗試自動定位（需授權）"):
        pos = get_user_location()
        if pos:
            st.session_state["user_pos"] = pos
            st.success(f"✅ 已自動定位成功：{pos}")
        else:
            st.warning("⚠️ 無法取得定位，請確認瀏覽器已授權，或改用手動輸入")

    lat = st.number_input("🔢 手動輸入緯度", format="%.6f", value=25.0173)
    lng = st.number_input("🔢 手動輸入經度", format="%.6f", value=121.5398)
    if st.button("✅ 使用手動輸入座標"):
        st.session_state["user_pos"] = (lat, lng)
        st.success(f"✅ 已設定自訂位置：({lat}, {lng})")

# === 導航按鈕 ===
if st.button("🚀 導航到最近地點"):
    user_pos = st.session_state["user_pos"]
    if not user_pos:
        st.warning("⚠️ 尚未定位，請先取得目前位置")
    else:
        nearest = find_nearest(user_pos, filtered) if filtered else None
        if nearest:
            try:
                lat = float(nearest["lat"])
                lng = float(nearest["lng"])
                target_pos = (lat, lng)
                st.session_state["route_coords"] = get_route(user_pos, target_pos, profile)
                st.success(f"🎯 已產生路線 → {nearest['name']}")
            except Exception as e:
                st.session_state["route_coords"] = []
                st.error(f"❌ 無法計算路線：{e}")

# === 分欄（地圖 + 評分）===
col1, col2 = st.columns([3, 1])

with col1:
    m = folium.Map(location=[25.0173, 121.5398], zoom_start=17, tiles="OpenStreetMap")

    for place in filtered:
        try:
            lat = float(place["lat"])
            lng = float(place["lng"])
        except:
            continue

        name = place["name"]
        type_ = place.get("type", "").strip().lower()
        ratings_raw = place.get("ratings", "")
        rating = calculate_average(ratings_raw)

        icon_color = "gray"
        if type_ == "restaurant":
            icon_color = "green"
        elif type_ == "toilet":
            icon_color = "blue"

        popup = f"<b>{name}</b><br>類型: {type_}<br>平均評分: {rating}"
        folium.Marker([lat, lng], popup=popup, icon=folium.Icon(color=icon_color)).add_to(m)

    user_pos = st.session_state.get("user_pos")
    route_coords = st.session_state.get("route_coords", [])

    if user_pos:
        folium.Marker(user_pos, tooltip="你的位置", icon=folium.Icon(color="cadetblue")).add_to(m)
    if route_coords:
        folium.PolyLine([(lat, lng) for lng, lat in route_coords], color="red", weight=5).add_to(m)

    st_folium(m, width=1400, height=600)

with col2:
    st.subheader("⭐ 立即評分")
    if filtered:
        place_options = [p["name"] for p in filtered]
        selected = st.selectbox("請選擇地點", place_options)
        score = st.slider("請給出評分 (1~5)", 1, 5)

        if st.button("送出評分"):
            add_rating(selected, score)
            st.success(f"✅ {selected} 評分成功：{score} 分")
    else:
        st.info("請先選擇有地點的分類")

    # === 顯示定位結果 ===
    user_pos = st.session_state.get("user_pos")
    if user_pos:
        st.markdown("### 📍 目前定位結果")
        st.write(f"緯度：`{user_pos[0]}`，經度：`{user_pos[1]}`")
    else:
        st.markdown("### 📍 尚未定位")
        st.info("請在上方定位或手動輸入座標")
