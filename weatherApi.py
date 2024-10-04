import requests as rq
import json
API_KEY = ""

def get_city_location(city_name):
    # Requesting api
    try:
      response = rq.get(f"http://api.openweathermap.org/geo/1.0/direct?q={city_name}&limit=3&appid={API_KEY}")
    except:
       print("Error connecting to API")

    # Checking if request went good
    if response.status_code == 200:
        data = response.json()

        if len(data) > 0:
            # Taking first element from api
            city_info = data[0]
            lat = city_info['lat']
            lon = city_info['lon']
            print(f'Pogoda dla miasta: {city_name}')
            # Returning city location
            return f'{lat} {lon}'
        else:
            print(f"Nie znaleziono lokalizacji dla miasta {city_name}.")
    else:
        print(f"Błąd w zapytaniu. Status code: {response.status_code}")
# Function that get data from api and printng it to the terminal
def get_weather(lat_lon):
   try:
      # Spliting location into lat and lon
      lat_lon = lat_lon.split()
      lat = lat_lon[0]
      lon = lat_lon[1]
      # Requesting api
      response = rq.get(f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={API_KEY}&lang=pl&units=metric")
      # Checking if api request went good
      if response.status_code == 200:
         data = response.json()
         # Checking if data from api is not empty
         if len(data) > 0:
               # Allign api data to variables
               weather_data = data['weather']
               weather = weather_data[0]
               desc = weather['description']

               main = data['main']
               temp = main['temp']
               temp_min = main['temp_min']
               temp_max = main['temp_max']

               wind = data['wind']
               wind_speed = wind['speed']
               # Printing to the terminal
               print(f'temperatura: {temp}°C\ntemperatura minimalna: {temp_min}°C\ntemperatura maksymalna: {temp_max}°C\nzachmurzenie: {desc}\nPrędkość wiatru: {wind_speed} km/s')
         else:
               print(f"Brak danych.")
      else:
         print(f"Błąd w zapytaniu. Status code: {response.status_code}")
   except:
      print("Błąd w lokalizacji")

get_weather(get_city_location(input("Podaj nazwe miasta\n")))
