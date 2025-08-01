from math import radians, sin, cos, sqrt, atan2
from .. import models
from . import notifications

def haversine(lat1, lon1, lat2, lon2):
    R = 6371.0  # Radius of Earth in kilometers

    lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])

    dlon = lon2 - lon1
    dlat = lat2 - lat1

    a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))

    distance = R * c
    return distance

def check_geofence(student: models.Student, geofences: list[models.Geofence]):
    for geofence in geofences:
        distance = haversine(
            float(student.latitude),
            float(student.longitude),
            float(geofence.latitude),
            float(geofence.longitude),
        )
        if distance <= geofence.radius:
            message = f"Your child, {student.name}, has entered the {geofence.name}."
            notifications.send_notification(student.parent.phone_number, message)
        else:
            message = f"Your child, {student.name}, has exited the {geofence.name}."
            notifications.send_notification(student.parent.phone_number, message)
