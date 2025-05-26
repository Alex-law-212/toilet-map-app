import streamlit as st

def get_user_location():
    st.markdown("## 手動輸入座標")
    lat = st.number_input("緯度", value=25.0173, format="%.6f", key="lat")
    lng = st.number_input("經度", value=121.5398, format="%.6f", key="lng")
    st.write(f"目前手動輸入的座標是：({lat}, {lng})")
    return (lat, lng)

pos = get_user_location()
st.write(f"取得座標: {pos}")
