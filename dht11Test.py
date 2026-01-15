import adafruit_dht
import board
import time

dht = adafruit_dht.DHT11(board.D4)   # DATA pini = GPIO4

while True:
    try:
        temp = dht.temperature
        hum = dht.humidity
        print(f"Sıcaklık: {temp}°C   Nem: {hum}%")
    except RuntimeError as e:
        print("Okuma hatası:", e)
    time.sleep(2)
