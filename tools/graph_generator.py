import matplotlib.pyplot as plt
import pandas as pd



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
    nom_graphique = "./images/Graphique " + title + ".png"
    plt.savefig(nom_graphique, bbox_inches="tight")  # sauvegarde du graphique
    plt.close()  # ferme le graphique pour éviter l'affichage
    return nom_graphique


