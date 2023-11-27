"""
BeadandoFeladat
"""
import toga
import httpx
from toga.style import Pack
from toga.style.pack import COLUMN
from pprint import pprint
from io import StringIO

class WeatherService:
    # Időjárás API szervíz
    api_key = "2735401ff43820e5c3a3e2a69b3bb9d6"
    base_url = "https://api.openweathermap.org/data/2.5/weather?q={city}&units=metric&appid="+api_key

    def __init__(self):
        pass

    def get_weather_data(self, city_name):
        # URL összeállítása
        complete_url = WeatherService.base_url.format(city=city_name)
        # HTTP hívás
        with httpx.Client() as client:
            response = client.get(complete_url)
        # Adat feldolgozás
        data = response.json()
        print(data)
        if data["cod"] != "404":
            city = data["name"]
            country = data["sys"]["country"]
            temp = data["main"]["temp"]
            feels_like = data["main"]["feels_like"]
            humidity = data["main"]["humidity"]
            wind_speed = data["wind"]["speed"]
            weather_desc = data["weather"][0]["description"]
            # Adat formázása
            weather_data = {
                "Város": city,
                "Ország": country,
                "Hőmérséklet": temp,
                "Hőérzet": feels_like,
                "Páratartalom": humidity,
                "Szélsebesség": wind_speed,
                "Leírás": weather_desc
            }
            formatted_string_io = StringIO()
            pprint(weather_data, stream=formatted_string_io, indent=2)
            formatted_string = formatted_string_io.getvalue()
            return formatted_string
        else:
            return None

class BeadandoBeeWare(toga.App):
    # Service létrehozása
    weather_service = WeatherService()
    
    def startup(self):

        # Konténer létrehozása
        # main_box = toga.MainWindow(title='Weather Info')
        main_box = toga.Box(style=Pack(direction=COLUMN))

        # Vizuális elemek deklarálása
        text_input = toga.TextInput()
        weather_button = toga.Button('Show weather!', on_press=lambda widget: self.show_weather_info(text_input.value))

        # Vizuális elemek hozzáadása a konténerhez
        main_box.add(text_input)
        main_box.add(weather_button)

        # Ablak összeállítása
        self.main_window = toga.MainWindow(title='Weather Info')
        self.main_window.content = main_box
        self.main_window.show()

    def show_weather_info(self, city):
        # Szervíz hívása
        result = BeadandoBeeWare.weather_service.get_weather_data(city)
        # Dialógus ablak nyitása
        self.main_window.info_dialog(
            'Weather update',
            result,
        )

def main():
    return BeadandoBeeWare()
