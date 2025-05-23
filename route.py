import openrouteservice
from openrouteservice import convert
from config import ORS_API_KEY

client = openrouteservice.Client(key=ORS_API_KEY)

def get_route(user_pos, target_pos, profile="foot-walking"):
    coords = [(user_pos[1], user_pos[0]), (target_pos[1], target_pos[0])]
    route = client.directions(coords, profile=profile)
    geometry = route["routes"][0]["geometry"]
    decoded = convert.decode_polyline(geometry)
    return decoded["coordinates"]
