import sqlite3
from datetime import datetime
import pandas as pd

DB_NAME = "app_history.db"

def init_db():
    with sqlite3.connect(DB_NAME) as conn:
        c = conn.cursor()
        c.execute('''
            CREATE TABLE IF NOT EXISTS weather_history (
                id INTEGER PRIMARY KEY,
                timestamp TEXT,
                city TEXT,
                temperature REAL,
                humidity INTEGER,
                wind_speed REAL
            )
        ''')
        c.execute('''
            CREATE TABLE IF NOT EXISTS calc_history (
                id INTEGER PRIMARY KEY,
                timestamp TEXT,
                operand1 REAL,
                operator TEXT,
                operand2 REAL,
                result REAL
            )
        ''')
        conn.commit()

def save_weather(city, temp, humidity, wind):
    with sqlite3.connect(DB_NAME) as conn:
        c = conn.cursor()
        c.execute('''
            INSERT INTO weather_history (timestamp, city, temperature, humidity, wind_speed)
            VALUES (?, ?, ?, ?, ?)
        ''', (datetime.now().isoformat(), city, temp, humidity, wind))
        conn.commit()

def save_calculation(x, op, y, result):
    with sqlite3.connect(DB_NAME) as conn:
        c = conn.cursor()
        c.execute('''
            INSERT INTO calc_history (timestamp, operand1, operator, operand2, result)
            VALUES (?, ?, ?, ?, ?)
        ''', (datetime.now().isoformat(), x, op, y, result))
        conn.commit()

def view_history(table):
    with sqlite3.connect(DB_NAME) as conn:
        c = conn.cursor()
        c.execute(f"SELECT * FROM {table}")
        return c.fetchall()

def export_calc_history_to_csv(filename='calc_history.csv'):
    with sqlite3.connect(DB_NAME) as conn:
        df = pd.read_sql_query("SELECT * FROM calc_history", conn)
        df.to_csv(filename, index=False)

def export_weather_history_to_csv(filename='weather_history.csv'):
    with sqlite3.connect(DB_NAME) as conn:
        df = pd.read_sql_query("SELECT * FROM weather_history", conn)
        df.to_csv(filename, index=False)

def clear_history(table):
    """Clear all records from the specified history table."""
    if table not in ['weather_history', 'calc_history']:
        raise ValueError("Invalid table name. Use 'weather_history' or 'calc_history'.")
    with sqlite3.connect(DB_NAME) as conn:
        c = conn.cursor()
        c.execute(f"DELETE FROM {table}")
        conn.commit()
