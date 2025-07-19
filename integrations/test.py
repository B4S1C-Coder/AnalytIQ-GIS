from integrations.openweather import OpenWeatherAPI
from dto.openweather import WeatherResponse

def test_get_current_weather_by_city_name(api: OpenWeatherAPI):
    weather_data: WeatherResponse | None = api.get_current_weather_by_city_name("Jaipur")

    assert isinstance(
        weather_data, WeatherResponse
    ), f"Unexpected weather_data type: {type(weather_data)}"

    print(weather_data)

if __name__ == "__main__":
    weather_api = OpenWeatherAPI()
    test_get_current_weather_by_city_name(weather_api)
