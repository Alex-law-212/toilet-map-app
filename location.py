import streamlit as st
from streamlit_geolocation import streamlit_geolocation
import pandas as pd

DATA_PATH = "data.csv"

def load_location_data():
    try:
        df = pd.read_csv(DATA_PATH)
        return df
    except Exception as e:
        st.error(f"讀取地點資料失敗：{e}")
        return pd.DataFrame(columns=["name", "lat", "lng"])

def calculate_distance(lat1, lng1, lat2, lng2):
    return ((lat1 - lat2)**2 + (lng1 - lng2)**2) ** 0.5

def find_nearest_place(lat, lng, df):
    if df.empty:
        return None
    df["distance"] = df.apply(lambda row: calculate_distance(lat, lng, row["lat"], row["lng"]), axis=1)
    nearest = df.loc[df["distance"].idxmin()]
    return nearest

def get_user_location():
    st.markdown("## 選擇定位方式")
    option = st.radio("請選擇定位方式", ["手機定位（GPS）", "手動輸入座標"])

    if option == "手機定位（GPS）":
        location = streamlit_geolocation()
        if location and location.get("latitude") and location.get("longitude"):
            lat = location["latitude"]
            lng = location["longitude"]
            st.success(f"GPS 定位成功：({lat:.6f}, {lng:.6f})")
        else:
            st.warning("無法取得 GPS 定位，請確認權限或使用手動輸入")
            return None
    else:
        lat = st.number_input("緯度", format="%.6f", value=25.0173, key="manual_lat")
        lng = st.number_input("經度", format="%.6f", value=121.5398, key="manual_lng")
        st.success(f"手動輸入座標：({lat:.6f}, {lng:.6f})")

    # 讀資料找最近點
    df = load_location_data()
    nearest = find_nearest_place(lat, lng, df)
    if nearest is not None:
        st.info(f"離你最近的地點是：**{nearest['name']}**，距離約 {nearest['distance']:.6f}")
    else:
        st.warning("找不到最近地點資料")

    return (lat, lng)
