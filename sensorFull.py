import smbus2
import time
import math
import adafruit_dht
import board
import serial

# gy271 
ADDRESS = 0x0D
bus = smbus2.SMBus(1)

# QMC5883L register adresleri
CTL_REG1 = 0x09
CTL_REG2 = 0x0A
SET_RESET = 0x0B

# dht11
dht = adafruit_dht.DHT11(board.D4)   # DATA pini = GPIO4

# nano baglantı
port = "/dev/ttyUSB0"
baud = 9600

ser = serial.Serial(port, baud, timeout=1)

def qmc5883l_init():
    bus.write_byte_data(ADDRESS, SET_RESET, 0x01)     # Software reset
    time.sleep(0.1)
    bus.write_byte_data(ADDRESS, CTL_REG1, 0x1D)      # Continuous mode, 200Hz, 2G, OSR=512
    time.sleep(0.1)

def read_raw():
    data = bus.read_i2c_block_data(ADDRESS, 0x00, 6)

    x = data[0] | (data[1] << 8)
    y = data[2] | (data[3] << 8)
    z = data[4] | (data[5] << 8)

    # signed conversion
    if x > 32767: x -= 65536
    if y > 32767: y -= 65536
    if z > 32767: z -= 65536

    return x, y, z

def heading_deg():
    x, y, z = read_raw()
    heading = math.degrees(math.atan2(y, x))
    if heading < 0:
        heading += 360
    return heading
    
    
def get_sensor_data():
    # Arduino verisi
    line =  ser.readline().decode('utf-8').strip()
    raw = voltage = current = sesVal = gasVal = None
    if line:
        try:
            raw, voltage, curent, sesVal, gasVal = line.split(",")
        except:
            pass

    # DHT11
    try:
        temp = dht.temperature
        hum = dht.humidity
    except:
        temp = None
        hum = None

    # Compass
    try:
        heading = read_heading()
    except:
        heading = None

    return {
        "voltage": voltage,
        "curent": curent,
        "sound": sesVal,
        "gas": gasVal,
        "tempp": temp,
        "hum": hum,
        "heading": heading
    }


qmc5883l_init()
time.sleep(2)  # Arduino’nun resetlenmesini bekle

while True:
    line = ser.readline().decode('utf-8').strip()
    if line:
        try:
            raw, voltage, current, sesVal, gasVal = line.split(",")
            print("Ham:", raw, " Volt:", voltage, "Akim:", current, " Ses:", sesVal, "Gas:", gasVal)
        except:
            print("Format hatası:", line)

    try:
        temp = dht.temperature
        hum = dht.humidity
        print(f"Sıcaklık: {temp}°C   Nem: {hum}%")
    except RuntimeError as e:
        print("DHT11 Okuma hatası:", e)

    try:
        print("Heading: {:.2f}°".format(heading_deg()))
    except Exception as e:
        print("GY-271 Read error:", e)
        
    print("------------------------------------------------")
