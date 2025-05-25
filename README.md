# 🌦️ Weather & Calculator Python App

A user-friendly Python application combining:
- Real-time **weather information** via OpenWeatherMap API 🌤️
- A basic **arithmetic calculator** ➕➖✖️➗
- A built-in **Tkinter GUI** 🖥️
- **SQLite database logging** 🗃️
- **CSV export** for reports 📄

---

## ✅ Features

### 🔹 Weather
- Get real-time weather info by city name
- Displays:
  - Temperature (°C)
  - Humidity (%)
  - Wind Speed (m/s)
- Logs queries to database
- Export weather history to `weather_history.csv`

### 🔹 Calculator
- Perform basic math operations:
  - Addition (`+`)
  - Subtraction (`-`)
  - Multiplication (`*`)
  - Division (`/`) with error handling
- Supports both integers and decimals
- Logs each calculation to database
- Export calculation history to `calc_history.csv`

### 🔹 User Interface
- **Graphical UI** (Tkinter tabs):
  - One tab for Weather
  - One tab for Calculator
- Error handling for invalid inputs and API failures

---

## 💻 Requirements

- Python 3.8+
- External Libraries:
  - `requests`
  - `pandas`

Install with:
```bash
pip install -r requirements.txt
## GUI Features (Tkinter)
- Weather lookup by city
- Simple calculator
- View saved weather and calculation history
- Export data to CSV
- Clear history records
