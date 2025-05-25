from history_manager import init_db, save_weather, save_calculation, view_history
from ui_gui import WeatherCalculatorApp
from weather_api import fetch_weather
from calculator import add, subtract, multiply, divide


def weather_menu():
    print("\nWeather Lookup")
    method = input("Search by (1) City or (2) Coordinates? ")

    try:
        if method == "1":
            city = input("Enter city name: ")
            weather = fetch_weather(city=city)
        elif method == "2":
            lat = float(input("Enter latitude: "))
            lon = float(input("Enter longitude: "))
            weather = fetch_weather(lat=lat, lon=lon)
        else:
            print("Invalid selection.")
            return

        print(f"\nWeather in {weather['location']}:")
        print(f"Temperature: {weather['temperature']} °C")
        print(f"Humidity: {weather['humidity']}%")
        print(f"Wind Speed: {weather['wind_speed']} m/s")

        save_weather(weather['location'], weather['temperature'], weather['humidity'], weather['wind_speed'])
    except Exception as e:
        print(f"Error: {e}")


def calculator_menu():
    print("\nSimple Calculator")
    try:
        x = float(input("Enter first number: "))
        op = input("Enter operation (+, -, *, /): ")
        y = float(input("Enter second number: "))

        if op == "+":
            result = add(x, y)
        elif op == "-":
            result = subtract(x, y)
        elif op == "*":
            result = multiply(x, y)
        elif op == "/":
            result = divide(x, y)
        else:
            print("Invalid operation.")
            return

        print(f"Result: {result}")
        save_calculation(x, op, y, result)
    except ValueError as e:
        print(f"Input error: {e}")
    except Exception as e:
        print(f"Calculation error: {e}")


def view_history_menu():
    table = input("View history from (weather / calc): ").strip().lower()
    if table in ["weather", "calc"]:
        records = view_history(f"{table}_history")
        for row in records:
            print(row)
    else:
        print("Invalid table name. Use 'weather' or 'calc'.")


def main():
    init_db()
    while True:
        print("\nMain Menu:")
        print("1. Weather Lookup")
        print("2. Calculator")
        print("3. View History")
        print("4. Launch GUI App")
        print("5. Exit")

        choice = input("Choose an option (1-5): ")

        if choice == "1":
            weather_menu()
        elif choice == "2":
            calculator_menu()
        elif choice == "3":
            view_history_menu()
        elif choice == "4":
            app = WeatherCalculatorApp()
            app.mainloop()
        elif choice == "5":
            print("Goodbye!")
            break
        else:
            print("Invalid option. Please try again.")


if __name__ == "__main__":
    main()
