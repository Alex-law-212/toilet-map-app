from streamlit_geolocation import streamlit_geolocation

def get_user_location():
    location = streamlit_geolocation()
    if location and location.get("latitude") and location.get("longitude"):
        return (location["latitude"], location["longitude"])
    return None
