from geopy.geocoders import Nominatim
from geopy.distance import geodesic
from .models import Coordinate
import re

geolocation = Nominatim(user_agent='your_app_name')

def parse_duration(duration_str):
    total_minutes = 0
    hours = re.search(r'(\d+)h', duration_str)
    minutes = re.search(r'(\d+)m', duration_str)
    if hours:
        total_minutes += int(hours.group(1)) * 60
    if minutes:
        total_minutes += int(minutes.group(1))
    return total_minutes

def create_coordinate(address):
    if not address:
        return None
    try:
        location = geolocation.geocode(address)
        if location:
            coordinate = Coordinate.objects.create(latitude=location.latitude, longitude=location.longitude)
            return coordinate
        else:
            return None
    except Exception as error:
        print(f"Error geocoding address: {error}")
        return None

def calculate_distance(point1, point2):
    distance_km = geodesic(point1, point2).kilometers
    return distance_km

def calculate_duration(point1, point2, speed_kmh=60):
    distance = calculate_distance(point1, point2)
    travel_time_hours = distance / speed_kmh
    
    hours = int(travel_time_hours)
    minutes = int((travel_time_hours - hours) * 60)
    return f"{hours}h {minutes}mins"


    