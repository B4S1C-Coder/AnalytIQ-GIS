import os
import requests
from dto.openweather import WeatherResponse, ForecastResponse
from dacite import from_dict

class OpenWeatherAPI:
    def __init__(self):
        self.__api_key: str | None = None

        if not self.refresh_api_key():
            raise RuntimeError("OPENWEATHER_API_KEY not set.")
        
        self.__current_weather_url = "https://api.openweathermap.org/data/2.5/weather"
        self.__forecast_weather_url = "https://api.openweathermap.org/data/2.5/forecast"

    def refresh_api_key(self) -> bool:
        temp_key = os.getenv("OPENWEATHER_API_KEY")

        if not temp_key:
            return False
        
        self.__api_key = temp_key
        return True
    
    def get_current_weather_by_city_name(self, city: str) -> WeatherResponse | None:
        url = f"{self.__current_weather_url}?q={city}&appid={self.__api_key}"
        response = requests.get(url)

        if response.status_code == 200:
            data = response.json()
            return from_dict(data_class=WeatherResponse, data=data)
        
        return None
    
    def get_forecast_by_city_name(self, city: str) -> ForecastResponse | None:
        url = f"{self.__forecast_weather_url}?q={city}&appid={self.__api_key}"
        response = requests.get(url)

        if response.status_code == 200:
            data = response.json()
            return from_dict(data_class=ForecastResponse, data=data)
        
        return None