#!/bin/bash

# Utwórz katalog /usr/share/fancontrol, jeśli nie istnieje
echo "Tworzenie katalogu /usr/share/fancontrol..."
sudo mkdir -p /usr/share/fancontrol

# Skopiuj pliki do /usr/share/fancontrol
echo "Kopiowanie plików do /usr/share/fancontrol..."
sudo cp fan.png fan.py /usr/share/fancontrol/

# Skopiuj plik .desktop do /usr/share/applications
echo "Kopiowanie pliku .desktop do /usr/share/applications..."
sudo cp fancontrol.desktop /usr/share/applications/

# Ustaw uprawnienia do pliku fan.py
echo "Ustawianie uprawnień..."
sudo chmod +x /usr/share/fancontrol/fan.py

echo "Instalacja zakończona pomyślnie!"