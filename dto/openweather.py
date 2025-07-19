from dataclasses import dataclass

@dataclass
class Coords:
    lon: float
    lat: float

@dataclass
class Weather:
    id: int
    main: str
    description: str
    icon: str

@dataclass
class Main:
    temp: float
    feels_like: float
    temp_min: float
    temp_max: float
    pressure: int
    humidity: int
    sea_level: int | None
    grnd_level: int | None

@dataclass
class Wind:
    speed: float
    deg: int
    gust: float | None

@dataclass
class Clouds:
    all: int

@dataclass
class Sys:
    country: str
    sunrise: int
    sunset: int

@dataclass
class WeatherResponse:
    coord: Coords
    weather: list[Weather]
    base: str
    main: Main
    visibility: int
    wind: Wind
    clouds: Clouds
    dt: int
    sys: Sys
    timezone: int
    id: int
    name: str
    cod: int