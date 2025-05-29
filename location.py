from streamlit_current_location import current_position

def get_user_location():
    """
    呼叫瀏覽器的 geolocation API，回傳使用者的座標 (latitude, longitude)，若失敗回傳 None。
    """
    location = current_position()

    if location and "latitude" in location and "longitude" in location:
        return (location["latitude"], location["longitude"])
    return None
