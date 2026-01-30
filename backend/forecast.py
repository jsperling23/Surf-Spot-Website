import requests
import json
#from db_class import Database


class PointForecast:
    def __init__(self, latitude: float, longitude: float):
        self._latitude = latitude
        self._longitude = longitude

    def get_point_forecast(self) -> dict:
        """
        Query the NOAA API a point forecast for the latitude and longitude
        """
        point_url = f'https://api.weather.gov/points/{self._latitude},{self._longitude}'
        point_response = requests.get(point_url)
        point_data = json.loads(point_response.text)
        forecast_url = point_data['properties']['forecastHourly']
        forecast_response = requests.get(forecast_url)
        forecast_data = json.loads(forecast_response.text)
        print(forecast_data)
        for key,value in forecast_data.items():
            print(key, value, "\n\n\n")


if __name__ == "__main__":
    point = PointForecast(37.6566, -122.4025)
    point.get_point_forecast()
