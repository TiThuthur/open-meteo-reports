import openmeteo_requests
import requests_cache, pandas as pd
from retry_requests import retry

#mise en place des différents outils utilisés
cache_session = requests_cache.CachedSession(".cache", expire_after=3600)
retry_session = retry(cache_session, retries=5,backoff_factor=0.2)
openmeteo = openmeteo_requests.Client(session=retry_session)

# url d'appel de l'Api
url = "https://api.open-meteo.com/v1/forecast"

# paramettres d'appel envoyés à l'API
params = {
    "latitude": 44.58184,#exemple pour plusieurs localisation [44.58184,44]
    "longitude": -0.039164,#exemple pour plusieurs localisation [-0.039164,-0,04]
    "hourly": ["temperature_2m","relative_humidity_2m"]
}
responses = openmeteo.weather_api(url, params=params)

response1 = responses[0]

print(f"Coordinates {response1.Latitude()}°N {response1.Longitude()}°E")
print(f"Elevation {response1.Elevation()} m asl")
print(f"Timezone {response1.Timezone()} {response1.TimezoneAbbreviation()}")
print(f"Timezone difference to GMT+0 {response1.UtcOffsetSeconds()} s")
