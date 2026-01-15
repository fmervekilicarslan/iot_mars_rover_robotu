import serial
import time

# Arduino portu (örnek: /dev/ttyUSB0)
port = "/dev/ttyUSB0"
baud = 9600

ser = serial.Serial(port, baud, timeout=1)
time.sleep(2)  # Arduino’nun resetlenmesini bekle

while True:
    line = ser.readline().decode('utf-8').strip()
    if line:
        try:
            raw, voltage, current, sesVal, gasVal = line.split(",")
            print("Ham:", raw, " Volt:", voltage, "Akim:", current, " Ses:", sesVal, "Gas:", gasVal )
        except:
            print("Format hatası:", line)

