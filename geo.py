from geopy.distance import geodesic

def find_nearest(user_pos, locations):
    return min(locations, key=lambda p: geodesic(user_pos, (p["lat"], p["lng"])).km)
