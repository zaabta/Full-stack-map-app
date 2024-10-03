from django.conf import settings
import googlemaps
from .models import Coordinate
import re

gmaps = googlemaps.Client(key=settings.GOOGLE_MAPS_API_KEY)

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

def calculate_duration(point1, point2):
    res = gmaps.distance_matrix(origins=[point1], destinations=[point2], mode='driving')
    if res['status'] != 'OK':
        raise ValueError("Error fetching data from Google Maps API")
    duration = res['rows'][0]['elements'][0]['duration']['value']
    hours, remainder = divmod(duration, 3600)
    minutes, _ = divmod(remainder, 60)
    return f'{hours}h {minutes}m'

def calculate_distance(point1, point2):
    res = gmaps.distance_matrix(origins=[point1], destinations=[point2], mode='driving')
    if res['status'] != 'OK':
        raise ValueError("Error fetching data from Google Maps API")
    distance_meters = re['rows'][0]['elements'][0]['distance']['value']
    return round(distance_meters / 1000, 2)

def parse_duration(duration_str):
    total_minutes = 0
    parts = duration_str.split()
    for part in parts:
        if 'h' in part:
            hours = int(part.replace('h', '').strip())
            total_minutes += hours * 60
        elif 'm' in part:
            minutes = int(part.replace('m', '').strip())
            total_minutes += minutes
            
    return total_minutes


def sort_orders(orders):
    return sorted(orders, key=lambda order: parse_duration(order.duration))
