from integrations.openweather import OpenWeatherAPI
from dto.openweather import WeatherResponse, ForecastResponse

def test_get_current_weather_by_city_name(api: OpenWeatherAPI):
    weather_data: WeatherResponse | None = api.get_current_weather_by_city_name("Jaipur")

    assert isinstance(
        weather_data, WeatherResponse
    ), f"Unexpected weather_data type: {type(weather_data)}"

    print(weather_data)

def test_get_forecast_by_city_name(api: OpenWeatherAPI):
    forecast_data: ForecastResponse | None = api.get_forecast_by_city_name("Jaipur")

    assert isinstance(
        forecast_data, ForecastResponse
    ), f"Unexpected forecast_data type: {type(forecast_data)}"

    print(forecast_data)

if __name__ == "__main__":
    weather_api = OpenWeatherAPI()
    test_get_current_weather_by_city_name(weather_api)

    print(" ----------------------------- ")

    test_get_forecast_by_city_name(weather_api)
