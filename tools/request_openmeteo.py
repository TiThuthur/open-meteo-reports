
import numpy as np

import pandas as pd



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




