import os
import tkinter as tk
from tkinter import ttk

# Ścieżki do plików PWM i temperatury CPU
PWM1_PATH = "/sys/class/hwmon/hwmon7/pwm1"
PWM2_PATH = "/sys/class/hwmon/hwmon7/pwm2"
FAN1_SPEED_PATH = "/sys/class/hwmon/hwmon7/fan1_input"
FAN2_SPEED_PATH = "/sys/class/hwmon/hwmon7/fan2_input"
TEMP_PATH = "/sys/class/hwmon/hwmon7/temp1_input"  # Ścieżka do odczytu temperatury CPU

# Stałe dla trybu półautomatycznego
TEMP_THRESHOLDS = {
    60: 900,   # Poniżej 60°C: 900 RPM
    80: 1500,  # 60-80°C: 1500 RPM
    100: 2500  # Powyżej 80°C: 2500 RPM
}

# Zmienna globalna do przechowywania trybu pracy
current_mode = "manual"  # Domyślnie tryb ręczny

def set_fan_speed(value, pwm_path):
    """ Ustawia prędkość wentylatora w zakresie 0-255 (odwrotnie) """
    pwm_value = int((100 - float(value)) * 255 / 100)  # Odwrócenie skali
    if pwm_value < 10:
        pwm_value = 0  # Zapewniamy pełne wyłączenie wentylatora, jeśli obsługuje
    try:
        with open(pwm_path, "w") as pwm:
            pwm.write(str(pwm_value))
    except PermissionError:
        print("Brak uprawnień! Uruchom skrypt jako root.")
    except FileNotFoundError:
        print(f"Nie znaleziono pliku {pwm_path}. Sprawdź poprawność ścieżek.")

def get_fan_speed(fan_path):
    """ Odczytuje aktualną prędkość wentylatora """
    try:
        with open(fan_path, "r") as fan:
            return fan.read().strip() + " RPM"
    except FileNotFoundError:
        return "Brak danych"

def get_cpu_temperature():
    """ Odczytuje temperaturę CPU """
    try:
        with open(TEMP_PATH, "r") as temp_file:
            temp = int(temp_file.read().strip()) / 1000  # Przelicz na stopnie Celsjusza
            return temp
    except FileNotFoundError:
        return None

def update_fan_speeds():
    """ Aktualizuje wyświetlane prędkości wentylatorów """
    fan1_speed_label.config(text=f"Wentylator 1: {get_fan_speed(FAN1_SPEED_PATH)}")
    fan2_speed_label.config(text=f"Wentylator 2: {get_fan_speed(FAN2_SPEED_PATH)}")
    root.after(1000, update_fan_speeds)  # Odświeżanie co sekundę

def update_pwm1(value):
    """ Aktualizuje prędkość wentylatora 1 w trybie ręcznym """
    if current_mode == "manual":
        pwm1_value_label.config(text=f"{int(float(value))}%")
        set_fan_speed(float(value), PWM1_PATH)

def update_pwm2(value):
    """ Aktualizuje prędkość wentylatora 2 w trybie ręcznym """
    if current_mode == "manual":
        pwm2_value_label.config(text=f"{int(float(value))}%")
        set_fan_speed(float(value), PWM2_PATH)

def auto_fan_control():
    """ Automatycznie reguluje prędkość wentylatorów na podstawie temperatury CPU """
    if current_mode == "semi_auto":
        temp = get_cpu_temperature()
        if temp is not None:
            if temp < 60:
                speed = TEMP_THRESHOLDS[60]
            elif 60 <= temp < 80:
                speed = TEMP_THRESHOLDS[80]
            else:
                speed = TEMP_THRESHOLDS[100]
            # Ustaw prędkość dla obu wentylatorów
            set_fan_speed((speed / 2500) * 100, PWM1_PATH)  # Przelicz na procenty
            set_fan_speed((speed / 1800) * 100, PWM2_PATH)
    elif current_mode == "full_auto":
        temp = get_cpu_temperature()
        if temp is not None:
            # Liniowe sterowanie prędkością
            speed = min(max(int((temp - 30) * 5), 0), 100)  # Przykład: 30°C = 0%, 50°C = 100%
            set_fan_speed(speed, PWM1_PATH)
            set_fan_speed(speed, PWM2_PATH)
    root.after(1000, auto_fan_control)  # Sprawdzaj temperaturę co 1 sekundę

def toggle_mode():
    """ Przełącza tryb pracy między ręcznym, półautomatycznym a pełnym automatycznym """
    global current_mode
    if current_mode == "manual":
        current_mode = "semi_auto"
        mode_button.config(text="Tryb: Półautomatyczny")
        pwm1_slider.config(state="disabled")
        pwm2_slider.config(state="disabled")
    elif current_mode == "semi_auto":
        current_mode = "full_auto"
        mode_button.config(text="Tryb: Pełny automatyczny")
        pwm1_slider.config(state="disabled")
        pwm2_slider.config(state="disabled")
    else:
        current_mode = "manual"
        mode_button.config(text="Tryb: Ręczny")
        pwm1_slider.config(state="normal")
        pwm2_slider.config(state="normal")

# Tworzenie głównego okna aplikacji
root = tk.Tk()
root.title("Sterowanie Wentylatorami")
root.geometry("500x400")  # Zwiększony rozmiar okna

# Przycisk do przełączania trybu pracy
mode_button = ttk.Button(root, text="Tryb: Ręczny", command=toggle_mode)
mode_button.pack(pady=20)  # Większy odstęp

# Suwak dla PWM1
pwm1_label = ttk.Label(root, text="Wentylator 1", font=("Arial", 12))
pwm1_label.pack(pady=10)
pwm1_slider = ttk.Scale(root, from_=0, to=100, orient="horizontal", command=update_pwm1, length=300)
pwm1_slider.pack(pady=10)
pwm1_value_label = ttk.Label(root, text="0%", font=("Arial", 12))
pwm1_value_label.pack(pady=10)

# Suwak dla PWM2
pwm2_label = ttk.Label(root, text="Wentylator 2", font=("Arial", 12))
pwm2_label.pack(pady=10)
pwm2_slider = ttk.Scale(root, from_=0, to=100, orient="horizontal", command=update_pwm2, length=300)
pwm2_slider.pack(pady=10)
pwm2_value_label = ttk.Label(root, text="0%", font=("Arial", 12))
pwm2_value_label.pack(pady=10)

# Etykiety z aktualną prędkością obrotową
fan1_speed_label = ttk.Label(root, text="Wentylator 1: Brak danych", font=("Arial", 12))
fan1_speed_label.pack(pady=10)
fan2_speed_label = ttk.Label(root, text="Wentylator 2: Brak danych", font=("Arial", 12))
fan2_speed_label.pack(pady=10)

# Uruchomienie aktualizacji prędkości wentylatorów
update_fan_speeds()

# Uruchomienie automatycznej kontroli wentylatorów
auto_fan_control()

# Uruchomienie aplikacji
root.mainloop()
