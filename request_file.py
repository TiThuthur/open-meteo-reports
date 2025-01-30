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

response1 = responses[0] #Prends le premier résultat, pour plusieurs localisation utiliser [n]

print(f"Coordinates {response1.Latitude()}°N {response1.Longitude()}°E")
print(f"Elevation {response1.Elevation()} m asl")
print(f"Timezone {response1.Timezone()} {response1.TimezoneAbbreviation()}")
print(f"Timezone difference to GMT+0 {response1.UtcOffsetSeconds()} s")

hourly = response1.Hourly()

hourly_temperature_2m = hourly.Variables(0).ValuesAsNumpy() #renvoi temperature_2m car premier argument de hourly
hourly_relative_humidity_2m = hourly.Variables(1).ValuesAsNumpy()#renvoi relative_humidity_2m car second argument de hourly

hourly_temperature_2m_data = {"date":pd.date_range(
    start=pd.to_datetime(hourly.Time(), unit="s", utc=True),#début de la ligne temporel
    end=pd.to_datetime(hourly.TimeEnd(), unit="s", utc=True),#fin de la ligne temporel
    freq=pd.Timedelta(seconds=hourly.Interval()),#Interval entre les records
    inclusive="left"
)}
hourly_temperature_2m_data["temperature_2m"] = hourly_temperature_2m
hourly_temperature_2m_dataFrame = pd.DataFrame(data=hourly_temperature_2m_data)#création d'un dataFrame à partir du dict précédement créé
print(hourly_temperature_2m_dataFrame.head())#affichage des 5 premières ligne du dataFrame
