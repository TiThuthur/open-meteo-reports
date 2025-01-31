import matplotlib.pyplot as plt
import numpy as np
import openmeteo_requests
import pandas as pd
import requests_cache
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from retry_requests import retry


def create_numpy_from_hourly(hourly_from_response, index: int) -> np.ndarray:
    """
    create a numpy array from hourly data
    :param hourly_from_response: response of open_meteo.weather_api(url, params=params)
    :param index: index of the collumn in hourly_from_response
    :return: a numpy array of the hourly data [n]
    """
    return hourly_from_response.Variables(index).ValuesAsNumpy()


def create_date_dict(hourly_function) -> dict:
    """
    create a dictionnary of dates
    :param hourly_function: houly section of the response
    :return: a dictionnary of dates with panda format
    """
    return {"date": pd.date_range(
        start=pd.to_datetime(hourly_function.Time(), unit="s", utc=True),  # début de la ligne temporel
        end=pd.to_datetime(hourly_function.TimeEnd(), unit="s", utc=True),  # fin de la ligne temporel
        freq=pd.Timedelta(seconds=hourly_function.Interval()),  # Interval entre les records
        inclusive="left"
    )}


def create_a_linear_graph(hourly_dataframe: pd.DataFrame, collumn: str, title: str, ylabel: str, color: str) -> str:
    """
    Create a graph of the hourly data
    :param color:
    :param hourly_dataframe: DataFrame containing hourly data
    :param collumn: Column name of the hourly data
    :param title: title of the graph
    :param ylabel: label in relation of the collumn
    :return: the name of the graph
    """
    # taille de la figure
    plt.figure(figsize=(20, 10))

    # création des ligne du graphique
    plt.plot(hourly_dataframe["date"], hourly_dataframe[collumn], color=color, marker="o", linestyle="-",
             label=ylabel)

    # Ajouter un titre et des labels
    plt.title(title)
    plt.xlabel("Date")  # ici toujours date
    plt.ylabel(ylabel)  # ici on entre le label de la colonne souhaité
    plt.xticks(rotation=90)

    # ajoute une légende
    plt.legend()
    nom_graphique = "Graphique " + title + ".png"
    plt.savefig(nom_graphique, bbox_inches="tight")  # sauvegarde du graphique
    plt.close()  # ferme le graphique pour éviter l'affichage
    return nom_graphique
def create_a_gradient_graph(hourly_dataframe: pd.DataFrame, collumn: str, title: str):

    temperature_matrix = np.array(hourly_dataframe[collumn]).reshape(-1, 1)
    #plt.figure(figsize=(20, 10))
    fig,ax = plt.subplots()
    im = ax.imshow(temperature_matrix,cmap="coolwarm", aspect="auto")
    ax.set_yticks(range(len(hourly_dataframe)))
    ax.set_yticklabels(hourly_dataframe["date"])
    cbar = plt.colorbar(im, ax=ax)
    cbar.set_label("Température (°C)")
    plt.show()

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
    "hourly": ["temperature_2m", "relative_humidity_2m","apparent_temperature"]
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

# 4 --- création des graphiques
nom_graphique1 = create_a_linear_graph(hourly_dataFrame, "temperature_2m", "Évolution de la température", "Température °C",
                                "red")
nom_graphique2 = create_a_linear_graph(hourly_dataFrame, "relative_humidity_2m", "Évolution de l'humidité", "Humidité %",
                                "blue")
nom_graphique3=create_a_linear_graph(hourly_dataFrame, "apparent_temperature", "Évolution de la température apparente", "Température °C", "green")

create_a_gradient_graph(hourly_dataFrame,"temperature_2m","Évolution de la température")
# 5 --- création du pdf
pdf_filename = "rapport.pdf"
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
