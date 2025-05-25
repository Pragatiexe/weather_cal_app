from history_manager import save_weather, save_calculation, view_history

save_weather("TestCity", 25.0, 60, 5.0)

save_calculation(10, "+", 5, 15)

print("Weather history:", view_history("weather_history"))
print("Calc history:", view_history("calc_history"))
