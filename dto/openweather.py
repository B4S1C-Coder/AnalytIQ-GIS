from dataclasses import dataclass, field
from dataclasses_json import dataclass_json, config

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
    temp_kf: float | None

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

@dataclass
class ForecastResponseSys:
    pod: str

@dataclass_json
@dataclass
class Rain:
    h3: float | None = field(default=None, metadata=config(field_name="3h"))

@dataclass_json
@dataclass
class Snow:
    h3: float | None = field(default=None, metadata=config(field_name="3h"))

@dataclass
class City:
    id: int
    name: str
    coord: Coords
    country: str
    population: int
    timezone: int
    sunrise: int
    sunset: int

@dataclass
class ForecastResponseListElement:
    dt: int
    main: Main
    weather: list[Weather]
    clouds: Clouds
    wind: Wind
    visibility: int
    pop: float
    dt_txt: str
    sys: ForecastResponseSys
    rain: Rain | None
    snow: Snow | None

@dataclass
class ForecastResponse:
    cod: str
    message: float
    cnt: int
    list: list[ForecastResponseListElement] # actual key is "list"
    city: City