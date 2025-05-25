from weather_api import fetch_weather

try:
    data = fetch_weather("London")
    print("Weather Data:", data)
except Exception as e:
    print("Error:", e)
