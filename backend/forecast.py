import requests
import json


class PointForecast:
    def __init__(self, latitude: float, longitude: float):
        self._latitude = latitude
        self._longitude = longitude

    def get_point_forecast(self) -> list[dict]:
        """
        Query the NOAA API a point forecast for the latitude and longitude and
        pack response into a dictionary.

        A failed request will return and empty dictionary.
        A successful request return a dictionary with the following format:
        [
            {"meta": str},  # timestamp when forecast was retrieved (ISO8601)
            {"number": int, # Hour from request, (1, 2, 3, ...), 1 is hour zero
             "time": str,          # ISO8601 datetime string with timezone
             "temperature": str,   # temperature value
             "temp_unit": str,     # temperature unit, e.g., 'F'
             "wind_speed": str,    # wind speed, e.g., '7 mph'
             "wind_dir": str,      # wind direction, e.g., 'NW'
              "weather": str       # short weather description
            },
            ...
        ]
        """
        completed_forecast = []
        point_url = f'https://api.weather.gov/points/{self._latitude},\
                    {self._longitude}'

        try:
            point_response = requests.get(point_url)
            point_data = json.loads(point_response.text)

            forecast_url = point_data['properties']['forecastHourly']
            forecast_response = requests.get(forecast_url)
            forecast_data = json.loads(forecast_response.text)

            times = forecast_data["properties"]["periods"]
            completed_forecast.append(
                {"meta": forecast_data["properties"]["generatedAt"]})

            for i in range(10):
                completed_forecast.append({})
                completed_forecast[i]["number"] = times[i]["number"]
                completed_forecast[i]["time"] = \
                    times[i]["startTime"]
                completed_forecast[i]["temperature"] = \
                    times[i]["temperature"]
                completed_forecast[i]["temp_unit"] = \
                    times[i]["temperatureUnit"]
                completed_forecast[i]["wind_speed"] = \
                    times[i]["windSpeed"]
                completed_forecast[i]["wind_dir"] = \
                    times[i]["windDirection"]
                completed_forecast[i]["weather"] = \
                    times[i]["shortForecast"]

        except requests.exceptions.HTTPError as http_err:
            print(f"HTTP error occurred: {http_err}")

        except requests.exceptions.ConnectionError as conn_err:
            print(f"Connection error occurred: {conn_err}")

        except requests.exceptions.Timeout as timeout_err:
            print(f"Request timed out: {timeout_err}")

        except json.JSONDecodeError as json_err:
            print(f"Error decoding JSON: {json_err}")

        except Exception as err:
            print(f"An unexpected error occurred: {err}")

        finally:
            return completed_forecast


if __name__ == "__main__":
    point = PointForecast(37.6566, -122.4025)
    print(point.get_point_forecast())
