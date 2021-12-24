import requests
from datetime import datetime

class Forecast:

    def __init__(self):
        self.api_url = 'https://api.openweathermap.org/data/2.5/weather'
        self.api_ur2 = 'https://api.openweathermap.org/data/2.5/weather'
        self.city = "x"

    def set_city(self, city):
        self.city = city


    def get_data(self):
        params = {
            'q': self.city,  # Lviv',
            'appid': '8552bf33f45bc1e900bf5f24411606c6',
            'units': 'metric'
        }

        res = requests.get(self.api_url, params=params)
        self.data = res.json()
        # template = 'Current temperature in {} is {}'
        # print(template.format(city, data['main']['temp']))
        return self.data


f = Forecast()
f.set_city("Khotyn")
print(f.get_data()["weather"][0]["main"])



"""
print(
    "Weather in "+ str(f.city) +" ("+str(f.get_data()['sys']['country'])+")\n" +
    "Date " + str(datetime.fromtimestamp(f.get_data()['dt']).strftime('%d-%m-%Y, checking time: %H:%M:%S')) + "\n" +
    "Minimal temperature: " + str(f.get_data()['main']['temp_min']) + "\n" +
    "Maximal temperature: " + str(f.get_data()['main']['temp_max']) + "\n" +
    "Humidity: " + str(f.get_data()['main']['humidity']) + "\n" +
    "Sunrise time: " + str(datetime.fromtimestamp(f.get_data()['sys']['sunrise']).strftime('%H:%M:%S')) + "\n" +
    "Sunset time: " + str(datetime.fromtimestamp(f.get_data()['sys']['sunset']).strftime('%H:%M:%S')) + "\n"
)

"""

#dd = ToDay("Khotyn")
#print(dd.data)
#print("temperature = " + str(dd.data["main"]["temp"]))
#print("temperature = " + str(dd.data["weather"][0]["main"]))
