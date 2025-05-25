import requests
from config import API_KEY

def fetch_weather(city=None):
    if not city:
        raise ValueError("City name is required.")
    
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"
    response = requests.get(url)

    if response.status_code != 200:
        raise Exception("Failed to fetch weather data. Check your city name or API key.")
    
    data = response.json()
    return {
        "location": data["name"],
        "temperature": data["main"]["temp"],
        "humidity": data["main"]["humidity"],
        "wind_speed": data["wind"]["speed"]
    }
