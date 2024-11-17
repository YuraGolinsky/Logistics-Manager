import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import json
import os
import requests

# Шлях до файлу для збереження маршрутів
ROUTES_FILE = "routes.json"

# Перевірка наявності файлу і його створення, якщо його немає
if not os.path.exists(ROUTES_FILE):
    with open(ROUTES_FILE, 'w') as file:
        json.dump([], file)

# Функція для завантаження маршрутів з JSON
def load_routes():
    with open(ROUTES_FILE, 'r', encoding='utf-8') as file:
        return json.load(file)

# Функція для збереження маршруту в JSON
def save_route(route_data):
    routes = load_routes()
    routes.append(route_data)
    with open(ROUTES_FILE, 'w', encoding='utf-8') as file:
        json.dump(routes, file, ensure_ascii=False, indent=4)

def get_weather_correction():
    try:
        response = requests.get(
            'https://api.openweathermap.org/data/2.5/weather?q=Kyiv&appid=abc123&units=metric')

        weather_data = response.json()
        temperature = weather_data['main']['temp']
        humidity = weather_data['main']['humidity']
        wind_speed = weather_data['wind']['speed']

        # Проста логіка корекції
        correction = 0
        if temperature < 0:
            correction += 15  # Збільшення на 15% в холодну погоду
        if humidity > 80:
            correction += 10  # Збільшення на 10% при високій вологості
        if wind_speed > 15:
            correction += 5  # Збільшення на 5% при сильному вітрі

        return correction

    except Exception as e:
        messagebox.showerror("Помилка", f"Не вдалося отримати дані про погоду: {e}")
        return 0


# Функція для розрахунку витрат пального
def calculate_fuel_cost(distance, fuel_consumption, baggage_weight, weather_correction):
    base_fuel = (distance / 100) * fuel_consumption
    fuel_for_baggage = baggage_weight * 0.05  # Припустимо, для багажу потрібно додавати 5% пального
    total_fuel = base_fuel + fuel_for_baggage
    total_fuel *= (1 + weather_correction / 100)
    return total_fuel

# Функція для розрахунку маршруту та збереження даних
def show_route_calculation(name_entry, pickup_entry, destination_entry, distance_entry, fuel_consumption_entry,
                           baggage_weight_entry, table):
    try:
        # Отримуємо дані з полів вводу
        distance_km = float(distance_entry.get())  # відстань
        fuel_consumption = float(fuel_consumption_entry.get())  # витрата пального
        baggage_weight = float(baggage_weight_entry.get())  # вага багажу

        weather_correction = get_weather_correction()

        # Автоматичний розрахунок загального кількості пального
        total_fuel = calculate_fuel_cost(distance_km, fuel_consumption, baggage_weight, weather_correction)

        route_data = {
            "name": name_entry.get(),
            "pickup": pickup_entry.get(),
            "destination": destination_entry.get(),
            "weight": baggage_weight,
            "distance": distance_km,
            "fuel_consumption": fuel_consumption,
            "weather_correction": weather_correction,
            "total_fuel": total_fuel
        }

        if not route_data["name"] or not route_data["pickup"] or not route_data["destination"]:
            messagebox.showerror("Помилка", "Всі поля повинні бути заповнені!")
            return

        save_route(route_data)
        update_table(table)

        result_text = f"""
        Розрахунок витрат пального:
        Ім'я: {route_data['name']}
        Відправлення: {route_data['pickup']}
        Призначення: {route_data['destination']}
        Відстань: {distance_km} км
        Витрати пального: {fuel_consumption} л/100 км
        Вага багажу: {baggage_weight} кг
        Корекція на погоду: {weather_correction} %
        Загальна кількість пального: {total_fuel:.2f} л
        """
        messagebox.showinfo("Розрахунок маршруту", result_text)

    except Exception as e:
        messagebox.showerror("Помилка", f"Сталася помилка: {e}")

# Функція для оновлення таблиці з маршрутами
def update_table(table):
    routes = load_routes()
    for row in table.get_children():
        table.delete(row)
    for route in routes:
        table.insert("", "end", values=(
            route['name'], route['pickup'], route['destination'], route['distance'],
            route['fuel_consumption'], route['total_fuel']))

# Основна функція main()
def main():
    root = tk.Tk()
    root.title("Маршрутний калькулятор")
    root.geometry("950x600")
    root.configure(bg="#f0f0f0")

    # Стиль для кнопок і полів вводу
    button_style = {'bg': '#007bff', 'fg': '#ffffff', 'font': ('Helvetica', 11), 'bd': 0, 'relief': 'flat'}
    entry_style = {'font': ('Helvetica', 12), 'bd': 1, 'relief': 'solid', 'width': 25, 'fg': '#000000'}
    label_style = {'font': ('Helvetica', 12), 'bg': '#f0f0f0'}

    # Введення імені
    name_label = tk.Label(root, text="Ім'я:", **label_style)
    name_label.grid(row=0, column=0, padx=10, pady=10)
    name_entry = tk.Entry(root, **entry_style)
    name_entry.grid(row=0, column=1, padx=10, pady=10)

    # Введення місця відправлення
    pickup_label = tk.Label(root, text="Звідки:", **label_style)
    pickup_label.grid(row=1, column=0, padx=10, pady=10)
    pickup_entry = tk.Entry(root, **entry_style)
    pickup_entry.grid(row=1, column=1, padx=10, pady=10)

    # Введення місця призначення
    destination_label = tk.Label(root, text="Куди:", **label_style)
    destination_label.grid(row=2, column=0, padx=10, pady=10)
    destination_entry = tk.Entry(root, **entry_style)
    destination_entry.grid(row=2, column=1, padx=10, pady=10)

    # Введення відстані
    distance_label = tk.Label(root, text="Відстань (км):", **label_style)
    distance_label.grid(row=3, column=0, padx=10, pady=10)
    distance_entry = tk.Entry(root, **entry_style)
    distance_entry.grid(row=3, column=1, padx=10, pady=10)

    # Введення витрат пального
    fuel_consumption_label = tk.Label(root, text="Витрати пального (л/100 км):", **label_style)
    fuel_consumption_label.grid(row=4, column=0, padx=10, pady=10)
    fuel_consumption_entry = tk.Entry(root, **entry_style)
    fuel_consumption_entry.grid(row=4, column=1, padx=10, pady=10)

    # Введення ваги багажу
    baggage_weight_label = tk.Label(root, text="Вага багажу (кг):", **label_style)
    baggage_weight_label.grid(row=5, column=0, padx=10, pady=10)
    baggage_weight_entry = tk.Entry(root, **entry_style)
    baggage_weight_entry.grid(row=5, column=1, padx=10, pady=10)

    # Кнопка розрахунку маршруту
    calculate_button = tk.Button(
        root,
        text="Розрахувати маршрут",
        command=lambda: show_route_calculation(
            name_entry,
            pickup_entry,
            destination_entry,
            distance_entry,
            fuel_consumption_entry,
            baggage_weight_entry,
            table
        ),
        **button_style
    )
    calculate_button.grid(row=6, columnspan=2, pady=20)

    # Створення таблиці для відображення маршрутів
    columns = ("Ім'я", "Звідки", "Куди", "Відстань (км)", "Витрати пального (л/100 км)", "Загальне пальне (л)")
    table = ttk.Treeview(root, columns=columns, show="headings", height=10)

    for col in columns:
        table.heading(col, text=col)
        table.column(col, anchor="center", width=150)

    table.grid(row=7, columnspan=2, padx=10, pady=10)

    root.mainloop()

if __name__ == "__main__":
    main()
