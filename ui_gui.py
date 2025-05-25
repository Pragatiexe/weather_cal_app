import tkinter as tk
from tkinter import ttk, messagebox
from weather_api import fetch_weather
from calculator import add, subtract, multiply, divide
from history_manager import (
    save_weather,
    save_calculation,
    init_db,
    export_calc_history_to_csv,
    export_weather_history_to_csv,
    view_history,
    clear_history
)

class WeatherCalculatorApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Weather & Calculator App")
        self.geometry("500x550")
        init_db()

        self.style = ttk.Style(self)
        self.style.theme_use('clam')

        self.logo_image = tk.PhotoImage(file="logo.png") if self._load_logo() else None
        if self.logo_image:
            tk.Label(self, image=self.logo_image).pack(pady=5)

        self.theme_var = tk.StringVar(value="Light")
        theme_frame = ttk.Frame(self)
        theme_frame.pack(pady=5)
        ttk.Label(theme_frame, text="Theme:").pack(side="left", padx=5)
        ttk.OptionMenu(theme_frame, self.theme_var, "Light", "Light", "Dark", command=self.toggle_theme).pack(side="left")

        tabs = ttk.Notebook(self)
        self.weather_tab = ttk.Frame(tabs)
        self.calc_tab = ttk.Frame(tabs)
        self.history_tab = ttk.Frame(tabs)

        tabs.add(self.weather_tab, text="Weather")
        tabs.add(self.calc_tab, text="Calculator")
        tabs.add(self.history_tab, text="View & Clear History")
        tabs.pack(expand=1, fill="both")

        self.build_weather_tab()
        self.build_calc_tab()
        self.build_history_tab()

    def _load_logo(self):
        try:
            with open("logo.png", "rb") as f:
                return True
        except FileNotFoundError:
            return False

    def toggle_theme(self, choice):
        if choice == "Dark":
            self.configure(bg="#2e2e2e")
            self.style.configure("TLabel", background="#2e2e2e", foreground="white")
            self.style.configure("TButton", background="#4a4a4a", foreground="white")
        else:
            self.configure(bg="SystemButtonFace")
            self.style.configure("TLabel", background="SystemButtonFace", foreground="black")
            self.style.configure("TButton", background="SystemButtonFace", foreground="black")

    def build_weather_tab(self):
        ttk.Label(self.weather_tab, text="City Name:").pack(pady=5)
        self.city_entry = ttk.Entry(self.weather_tab)
        self.city_entry.pack()

        ttk.Button(self.weather_tab, text="Get Weather", command=self.get_weather).pack(pady=10)

        self.weather_result = ttk.Label(self.weather_tab, text="", wraplength=300, justify="left")
        self.weather_result.pack()

        ttk.Button(self.weather_tab, text="Export Weather History", command=self.export_weather_csv).pack(pady=5)

    def get_weather(self):
        city = self.city_entry.get()
        try:
            data = fetch_weather(city=city)
            result = (
                f"Location: {data['location']}\n"
                f"Temperature: {data['temperature']} °C\n"
                f"Humidity: {data['humidity']}%\n"
                f"Wind Speed: {data['wind_speed']} m/s"
            )
            self.weather_result.config(text=result)
            save_weather(data['location'], data['temperature'], data['humidity'], data['wind_speed'])
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def build_calc_tab(self):
        self.entry1 = ttk.Entry(self.calc_tab)
        self.entry1.pack(pady=5)

        self.operator = ttk.Combobox(self.calc_tab, values=["+", "-", "*", "/"])
        self.operator.pack()

        self.entry2 = ttk.Entry(self.calc_tab)
        self.entry2.pack(pady=5)

        ttk.Button(self.calc_tab, text="Calculate", command=self.calculate).pack(pady=10)

        self.calc_result = ttk.Label(self.calc_tab, text="", wraplength=300)
        self.calc_result.pack()

        ttk.Button(self.calc_tab, text="Export Calc History", command=self.export_calc_csv).pack(pady=5)

    def calculate(self):
        try:
            x = float(self.entry1.get())
            y = float(self.entry2.get())
            op = self.operator.get()

            if op == "+":
                result = add(x, y)
            elif op == "-":
                result = subtract(x, y)
            elif op == "*":
                result = multiply(x, y)
            elif op == "/":
                result = divide(x, y)
            else:
                raise ValueError("Invalid operation")

            self.calc_result.config(text=f"Result: {result}")
            save_calculation(x, op, y, result)

        except Exception as e:
            messagebox.showerror("Error", str(e))

    def export_calc_csv(self):
        try:
            export_calc_history_to_csv()
            messagebox.showinfo("Export Successful", "Calc history exported to 'calc_history.csv'")
        except Exception as e:
            messagebox.showerror("Export Failed", str(e))

    def export_weather_csv(self):
        try:
            export_weather_history_to_csv()
            messagebox.showinfo("Export Successful", "Weather history exported to 'weather_history.csv'")
        except Exception as e:
            messagebox.showerror("Export Failed", str(e))

    def build_history_tab(self):
        self.table_choice = ttk.Combobox(self.history_tab, values=["weather", "calc"])
        self.table_choice.pack(pady=5)

        ttk.Button(self.history_tab, text="Display History", command=self.display_history).pack(pady=5)

        self.history_output = tk.Text(self.history_tab, height=15, width=50)
        self.history_output.pack(pady=5)

        ttk.Button(self.history_tab, text="Clear Selected History", command=self.clear_history_confirm).pack(pady=5)

    def display_history(self):
        table = self.table_choice.get()
        if table in ["weather", "calc"]:
            records = view_history(f"{table}_history")
            self.history_output.delete("1.0", tk.END)
            for row in records:
                self.history_output.insert(tk.END, f"{row}\n")
        else:
            messagebox.showwarning("Invalid Input", "Choose either 'weather' or 'calc'")

    def clear_history_confirm(self):
        table = self.table_choice.get()
        if table in ["weather", "calc"]:
            if messagebox.askyesno("Confirm", f"Clear all {table} history?"):
                clear_history(f"{table}_history")
                self.history_output.delete("1.0", tk.END)
                messagebox.showinfo("Cleared", f"{table.capitalize()} history cleared.")
        else:
            messagebox.showwarning("Invalid Input", "Choose either 'weather' or 'calc'")

if __name__ == "__main__":
    app = WeatherCalculatorApp()
    app.mainloop()
