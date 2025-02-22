#!/bin/bash

# Adres URL do repozytorium na GitHubie
REPO_URL="https://github.com/twoja_nazwa_użytkownika/twoje_repozytorium/archive/main.zip"

# Tymczasowy katalog do pobrania i rozpakowania plików
TMP_DIR=$(mktemp -d)

# Pobierz repozytorium jako zip
echo "Pobieranie repozytorium z GitHub..."
wget -q "$REPO_URL" -O "$TMP_DIR/repo.zip"

# Rozpakuj pliki
echo "Rozpakowywanie plików..."
unzip -q "$TMP_DIR/repo.zip" -d "$TMP_DIR"

# Przejdź do katalogu z rozpakowanymi plikami
cd "$TMP_DIR/$(basename "$REPO_URL" .zip)/fancontrol"

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

# Sprzątanie
echo "Czyszczenie tymczasowych plików..."
rm -rf "$TMP_DIR"

echo "Instalacja zakończona pomyślnie!"
