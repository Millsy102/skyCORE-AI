
import requests
import time
from threading import Thread

class WeatherAPI(Thread):
    def __init__(self, runtime, city="London", api_key="your_api_key"):
        super().__init__(daemon=True)
        self.runtime = runtime
        self.city = city
        self.api_key = api_key

    def run(self):
        while True:
            try:
                url = f"http://api.openweathermap.org/data/2.5/weather?q={self.city}&appid={self.api_key}&units=metric"
                r = requests.get(url)
                data = r.json()
                self.runtime.memory.add({"sensor": "weather", "data": data})
                temp = data['main']['temp']
                self.runtime.settings.set("weather_temp", temp)
            except:
    print('Weather fallback')
