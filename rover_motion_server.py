import asyncio
import websockets
import pigpio
import json

# =============================
# PIGPIO BAŞLAT
# =============================
pi = pigpio.pi()
if not pi.connected:
    raise RuntimeError("pigpio daemon çalışmıyor!")

# =============================
# MOTOR PINLERİ (BTS7960)
# =============================
RPWM1 = 26
LPWM1 = 16
RPWM2 = 15
LPWM2 = 18

motor_pins = [RPWM1, LPWM1, RPWM2, LPWM2]
for p in motor_pins:
    pi.set_mode(p, pigpio.OUTPUT)

# =============================
# SERVO PINLERİ
# =============================
SERVO_PIN3 = 25
SERVO_PIN4 = 24

pi.set_mode(SERVO_PIN3, pigpio.OUTPUT)
pi.set_mode(SERVO_PIN4, pigpio.OUTPUT)

# =============================
# AYARLAR
# =============================
SERVO_MIN_US = 500
SERVO_MAX_US = 2500

servo3_angle = 90
servo4_angle = 90

# =============================
# MOTOR FONKSİYONLARI
# =============================
def set_motor(r1, l1, r2, l2):
    pi.set_PWM_dutycycle(RPWM1, r1)
    pi.set_PWM_dutycycle(LPWM1, l1)
    pi.set_PWM_dutycycle(RPWM2, r2)
    pi.set_PWM_dutycycle(LPWM2, l2)

def stop():
    pi.set_PWM_dutycycle(RPWM1, 0)
    pi.set_PWM_dutycycle(LPWM1, 0)
    pi.set_PWM_dutycycle(RPWM2, 0)
    pi.set_PWM_dutycycle(LPWM2, 0)

def forward(speed):
    pi.set_PWM_dutycycle(RPWM1, 0)
    pi.set_PWM_dutycycle(LPWM1, speed)
    pi.set_PWM_dutycycle(RPWM2, speed)
    pi.set_PWM_dutycycle(LPWM2, 0)

def backward(speed):
    pi.set_PWM_dutycycle(RPWM1, speed)
    pi.set_PWM_dutycycle(LPWM1, 0)
    pi.set_PWM_dutycycle(RPWM2, 0)
    pi.set_PWM_dutycycle(LPWM2, speed)

def left(speed):
    pi.set_PWM_dutycycle(RPWM1, 0)
    pi.set_PWM_dutycycle(LPWM1, speed)
    pi.set_PWM_dutycycle(RPWM2, 0)
    pi.set_PWM_dutycycle(LPWM2, speed)

def right(speed):
    pi.set_PWM_dutycycle(RPWM1, speed)
    pi.set_PWM_dutycycle(LPWM1, 0)
    pi.set_PWM_dutycycle(RPWM2, speed)
    pi.set_PWM_dutycycle(LPWM2, 0)

# =============================
# SERVO FONKSİYONLARI
# =============================
def angle_to_pulse(angle):
    return SERVO_MIN_US + (SERVO_MAX_US - SERVO_MIN_US) * (angle / 180.0)

def set_servo(pin, angle):
    angle = max(0, min(180, angle))
    pulse = angle_to_pulse(angle)
    pi.set_servo_pulsewidth(pin, pulse)
    return angle

# Başlangıç pozisyonu
servo3_angle = set_servo(SERVO_PIN3, servo3_angle)
servo4_angle = set_servo(SERVO_PIN4, servo4_angle)

# =============================
# WEBSOCKET HANDLER
# =============================
async def handler(websocket):
    global servo3_angle, servo4_angle

    print("WebSocket bağlantısı alındı.")
    stop()  # güvenlik

    try:
        async for msg in websocket:
            data = json.loads(msg)
            cmd = data.get("cmd")
            speed = int(data.get("speed", 140))
            speed = max(0, min(speed, 255))
            step = int(data.get("step", 5))

            # ===== MOTOR =====
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

            # ===== SERVO 3 =====
            elif cmd == "servo3_add":
                servo3_angle = set_servo(SERVO_PIN3, servo3_angle + step)
            elif cmd == "servo3_sub":
                servo3_angle = set_servo(SERVO_PIN3, servo3_angle - step)

            # ===== SERVO 4 =====
            elif cmd == "servo4_add":
                servo4_angle = set_servo(SERVO_PIN4, servo4_angle + step)
            elif cmd == "servo4_sub":
                servo4_angle = set_servo(SERVO_PIN4, servo4_angle - step)

    except Exception as e:
        print("Bağlantı kesildi:", e)
        stop()

# =============================
# SERVER
# =============================
async def main():
    print("WebSocket aktif → ws://0.0.0.0:8766")
    async with websockets.serve(handler, "0.0.0.0", 8766):
        await asyncio.Future()

asyncio.run(main())
