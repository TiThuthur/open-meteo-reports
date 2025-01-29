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
    "latitude": 44.63998,
    "longitude": -0.796953,
    "hourly": "temperature_2m, relative_humidity_2m"
}
response = openmeteo.weather_api(url, params=params)
