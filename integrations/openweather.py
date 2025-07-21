import os
import requests
from dto.openweather import WeatherResponse, ForecastResponse
from integrations.tool_integrator import Tool
from dacite import from_dict

class OpenWeatherAPI(Tool):
    def __init__(self):
        super().__init__()
        self.__api_key: str | None = None

        if not self.refresh_api_key():
            raise RuntimeError("OPENWEATHER_API_KEY not set.")
        
        self.__current_weather_url = "https://api.openweathermap.org/data/2.5/weather"
        self.__forecast_weather_url = "https://api.openweathermap.org/data/2.5/forecast"

    def _set_exported_tool_docs(self) -> None:
        self.__exported_tool_descriptions = {
            "OpenWeatherAPI.get_current_weather_by_city_name": self.get_current_weather_by_city_name.__doc__,
            "OpenWeatherAPI.get_forecast_by_city_name": self.get_forecast_by_city_name.__doc__
        }

    def refresh_api_key(self) -> bool:
        temp_key = os.getenv("OPENWEATHER_API_KEY")

        if not temp_key:
            return False
        
        self.__api_key = temp_key
        return True
    
    def get_current_weather_by_city_name(self, city: str) -> WeatherResponse | None:
        """
        Tool: OpenWeatherAPI.get_current_weather_by_city_name
        Description: Get the current weather conditions for a gven city.
        Arguments:
            city (str): Name of the city.
        Returns:
            WeatherResponse object with temperature, humidity, wind, etc.
        """
        url = f"{self.__current_weather_url}?q={city}&appid={self.__api_key}"
        response = requests.get(url)

        if response.status_code == 200:
            data = response.json()
            return from_dict(data_class=WeatherResponse, data=data)
        
        return None
    
    def get_forecast_by_city_name(self, city: str) -> ForecastResponse | None:
        """
        Tool: OpenWeatherAPI.get_forecast_by_city_name
        Description: Get a 5-day / 3-hour forecast for a given city.
        Arguments:
            city (str): Name of the city.
        Returns:
            ForecastResponse object with future temperature, rain/snow and more.
        """
        url = f"{self.__forecast_weather_url}?q={city}&appid={self.__api_key}"
        response = requests.get(url)

        if response.status_code == 200:
            data = response.json()
            return from_dict(data_class=ForecastResponse, data=data)
        
        return None