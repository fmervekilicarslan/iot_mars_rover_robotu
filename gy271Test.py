import smbus2
import time
import math

ADDRESS = 0x0D
bus = smbus2.SMBus(1)

# QMC5883L register adresleri
CTL_REG1 = 0x09
CTL_REG2 = 0x0A
SET_RESET = 0x0B

# Initialization
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

qmc5883l_init()

while True:
    try:
        print("Heading: {:.2f}°".format(heading_deg()))
    except Exception as e:
        print("Read error:", e)

    time.sleep(0.2)
