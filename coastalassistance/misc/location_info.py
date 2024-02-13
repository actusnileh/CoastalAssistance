from geopy.geocoders import Nominatim


async def get_location_info(latitude, longitude):
    geolocator = Nominatim(user_agent="geo_locator")
    location = geolocator.reverse((latitude, longitude), language="ru")
    return location.address
