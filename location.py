from streamlit_geolocation import streamlit_geolocation

def get_user_location():
    location = streamlit_geolocation()
    if location and location.get("latitude") is not None and location.get("longitude") is not None:
        return (location["latitude"], location["longitude"])
    return None
