import smbus2
import time
import math
import adafruit_dht
import board
import serial
from datetime import datetime

# gy271
ADDRESS = 0x0D
bus = smbus2.SMBus(1)

CTL_REG1 = 0x09
SET_RESET = 0x0B

# dht11
dht = adafruit_dht.DHT11(board.D4)

# arduino
port = "/dev/ttyUSB0"
baud = 9600
ser = serial.Serial(port, baud, timeout=1)


def qmc_init():
    bus.write_byte_data(ADDRESS, SET_RESET, 0x01)
    time.sleep(0.1)
    bus.write_byte_data(ADDRESS, CTL_REG1, 0x1D)
    time.sleep(0.1)

qmc_init()


def read_heading():
    data = bus.read_i2c_block_data(ADDRESS, 0x00, 6)

    x = data[0] | (data[1] << 8)
    y = data[2] | (data[3] << 8)

    if x > 32767: x -= 65536
    if y > 32767: y -= 65536

    heading = math.degrees(math.atan2(y, x))
    if heading < 0:
        heading += 360
    return heading


def get_sensor_data():
    # Arduino verisi
    line = ser.readline().decode("utf-8").strip()
    raw = voltage = current = sesVal = gasVal = None
    if line:
        try:
            raw, voltage, current, sesVal, gasVal = line.split(",")
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
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "voltage": voltage,
        "current": current,
        "sound": sesVal,
        "gas": gasVal,
        "temp": temp,
        "hum": hum,
        "heading": heading
    }
