from gpiozero import DigitalInputDevice
from time import sleep

sensor = DigitalInputDevice(4)   # OUT → GPIO4

while True:
    if sensor.value == 0:
        print("Titreşim algılandı!")
    else:
        print("Sessiz...")
    sleep(0.2)
