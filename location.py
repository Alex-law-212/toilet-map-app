import streamlit as st
from streamlit_geolocation import streamlit_geolocation

def get_user_location():
    st.markdown("## 定位方式選擇")

    # 按鈕觸發手機定位
    if st.button("📍 手機自動定位（GPS）"):
        location = streamlit_geolocation()
        if location and location.get("latitude") and location.get("longitude"):
            lat = location["latitude"]
            lng = location["longitude"]
            st.session_state["user_pos"] = (lat, lng)
            st.success(f"✅ 已取得 GPS 定位：({lat:.6f}, {lng:.6f})")
        else:
            st.warning("⚠️ 無法取得 GPS 定位，請確認授權")

    # 手動輸入欄位
    st.markdown("或手動輸入座標：")
    lat = st.number_input("緯度", value=st.session_state.get("manual_lat", 25.0173), format="%.6f", key="manual_lat")
    lng = st.number_input("經度", value=st.session_state.get("manual_lng", 121.5398), format="%.6f", key="manual_lng")

    # 手動輸入送出按鈕
    if st.button("✅ 送出手動座標"):
        st.session_state["user_pos"] = (lat, lng)
        st.success(f"✅ 已設定手動座標：({lat:.6f}, {lng:.6f})")

    # 回傳目前定位結果或 None
    return st.session_state.get("user_pos", None)
