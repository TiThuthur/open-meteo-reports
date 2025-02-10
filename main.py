import openmeteo_requests
import pandas as pd
import requests_cache
from retry_requests import retry
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from tools.request_openmeteo import create_numpy_from_hourly, create_date_dict
from tools.graph_generator import create_a_linear_graph

# 1--- mise en place des différents outils utilisés
cache_session = requests_cache.CachedSession(".cache", expire_after=3600)
retry_session = retry(cache_session, retries=5, backoff_factor=0.2)
open_meteo = openmeteo_requests.Client(session=retry_session)

# url d'appel de l'Api
url = "https://api.open-meteo.com/v1/forecast"

# paramètres d'appel envoyés à l'API
params = {
    "latitude": 44.58184,  # exemple pour plusieurs localisation [44.58184,44]
    "longitude": -0.039164,  # exemple pour plusieurs localisation [-0.039164,-0,04]
    "hourly": ["temperature_2m", "relative_humidity_2m", "apparent_temperature"]
}

# 2 --- request à l'API
responses = open_meteo.weather_api(url, params=params)

# 3 --- traitement des données
response1 = responses[0]  # Prends le premier résultat, pour plusieurs localisation utiliser [n]
hourly = response1.Hourly()

hourly_data = create_date_dict(hourly)

hourly_data["temperature_2m"] = create_numpy_from_hourly(hourly, 0)  # créé un narray pour la température

hourly_data["relative_humidity_2m"] = create_numpy_from_hourly(hourly, 1)  # créé un narray pour l'humidité

hourly_data["apparent_temperature"] = create_numpy_from_hourly(hourly, 2)

hourly_dataFrame = pd.DataFrame(data=hourly_data)  # création d'un dataFrame à partir du dict précédement créé

# 4 --- création des graphiques dans le dossier images
nom_graphique1 = create_a_linear_graph(hourly_dataFrame, "temperature_2m", "Évolution de la température",
                                       "Température °C",
                                       "red")
nom_graphique2 = create_a_linear_graph(hourly_dataFrame, "relative_humidity_2m", "Évolution de l'humidité",
                                       "Humidité %",
                                       "blue")
nom_graphique3 = create_a_linear_graph(hourly_dataFrame, "apparent_temperature",
                                       "Évolution de la température apparente", "Température °C", "green")

# 5 --- création de raport.pdf
pdf_filename = "../rapports/rapport.pdf"
c = canvas.Canvas(pdf_filename, pagesize=letter)

# titre du rapport
c.drawString(200, 750, "Évolution de la température et de l'humidité")

# dessin de l'image
c.drawImage(nom_graphique1, 50, 400, width=500, height=300)
c.drawImage(nom_graphique2, 50, 50, width=500, height=300)

c.showPage()

c.drawImage(nom_graphique3, 50, 400, width=500, height=300)

c.save()  # Sauvegarde du PDF

print(f"📄 Rapport généré : {pdf_filename}")