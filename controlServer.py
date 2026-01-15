import asyncio
import websockets
import pigpio
import json

# =============================
# PIGPIO BAsLAT
# =============================
pi = pigpio.pi()
if not pi.connected:
    raise RuntimeError("pigpio daemon calismiyor!  sudo systemctl start pigpiod")

# =============================
# BTS7960 MOTOR PINLER?
# =============================
RPWM1 = 26
LPWM1 = 20
RPWM2 = 15
LPWM2 = 18

motor_pins = [RPWM1, LPWM1, RPWM2, LPWM2]
for p in motor_pins:
    pi.set_mode(p, pigpio.OUTPUT)

# =============================
# MOTOR KONTROL FONKSiYONLARI
# =============================

def set_motor(r1, l1, r2, l2):
    pi.set_PWM_dutycycle(RPWM1, r1)
    pi.set_PWM_dutycycle(LPWM1, l1)
    pi.set_PWM_dutycycle(RPWM2, r2)
    pi.set_PWM_dutycycle(LPWM2, l2)

def stop():
    set_motor(0, 0, 0, 0)

def forward(speed):
    set_motor(0, speed, speed, 0)

def backward(speed):
    set_motor(speed, 0, 0, speed)

def left(speed):
    set_motor(0, speed, 0, speed)

def right(speed):
    set_motor(speed, 0, speed, 0)
    
    
# ================ SERVO KONTROLLERi ====================
# ======================================================

SERVO_PIN3 = 25
SERVO_PIN4 = 17

pi.set_mode(SERVO_PIN3, pigpio.OUTPUT)
pi.set_mode(SERVO_PIN4, pigpio.OUTPUT)

SERVO_MIN_US = 500
SERVO_MAX_US = 2500

servo3_angle = 90
servo4_angle = 90

def angle_to_pulse(angle):
    return SERVO_MIN_US + (SERVO_MAX_US - SERVO_MIN_US) * (angle / 180.0)

def set_servo(pin, angle):
    angle = max(0, min(180, angle))
    pulse = angle_to_pulse(angle)
    pi.set_servo_pulsewidth(pin, pulse)
    return angle

# baglanti pozisyonu
set_servo(SERVO_PIN3, servo3_angle)
set_servo(SERVO_PIN4, servo4_angle)


# =============================
# WEBSOCKET HANDLER
# =============================
async def handler(websocket):
    print("WebSocket baglantisi saglandi.")

    stop()

    try:
        async for msg in websocket:

            try:
                data = json.loads(msg)
            except:
                print("JSON hatasi:", msg)
                continue

            cmd   = data.get("cmd", "")
            speed = int(data.get("speed", 140))

            speed = max(0, min(speed, 255))

            print("Komut:", cmd, "Hiz:", speed)

            if cmd == "forward":
                forward(speed)

            elif cmd == "backward":
                backward(speed)

            elif cmd == "left":
                left(speed)

            elif cmd == "right":
                right(speed)

            elif cmd == "stop":
                stop()
                
            elif cmd == "servo3_set":
                angle = int(data.get("angle", 90))
                servo3_angle = pi.set_servo_pulsewidth(SERVO_PIN3, angle_to_pulse(angle))

            elif cmd == "servo4_set":
                angle = int(data.get("angle", 90))
                servo4_angle = pi.set_servo_pulsewidth(SERVO_PIN4, angle_to_pulse(angle))

            elif cmd == "servo3_add":
                servo3_angle += int(data.get("step", 10))
                servo3_angle = pi.set_servo_pulsewidth(SERVO_PIN3, angle_to_pulse(servo3_angle))

            elif cmd == "servo3_sub":
                servo3_angle -= int(data.get("step", 10))
                servo3_angle = pi.set_servo_pulsewidth(SERVO_PIN3, angle_to_pulse(servo3_angle ))(

            elif cmd == "servo4_add":
                servo4_angle += int(data.get("step", 10))
                servo4_angle = set_servo(SERVO_PIN4, servo4_angle)

            elif cmd == "servo4_sub":
                servo4_angle -= int(data.get("step", 10))
                servo4_angle = set_servo(SERVO_PIN4, servo4_angle)

            elif cmd == "servo_reset":
                servo3_angle = set_servo(SERVO_PIN3, 90)
                servo4_angle = set_servo(SERVO_PIN4, 90)

            else:
                print("Tanimsiz komut:", cmd)

    except Exception as e:
        print("Baglanti kesildi:", e)
        stop()

async def main():
    print("WebSocket server aktif  ws://0.0.0.0:8765")
    async with websockets.serve(handler, "0.0.0.0", 8765):
        await asyncio.Future()

try:
    asyncio.run(main())
except KeyboardInterrupt:
    pi.set_servo_pulsewidth(SERVO_PIN1, 0)
    pi.set_servo_pulsewidth(SERVO_PIN2, 0)
    pi.set_servo_pulsewidth(SERVO_PIN3, 0)
    pi.set_servo_pulsewidth(SERVO_PIN4, 0)
    pi.stop()
    stop()
    print("Program durduruldu.")
