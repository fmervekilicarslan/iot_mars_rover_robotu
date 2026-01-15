import pigpio
import time

SERVO_PIN = 12          # BCM pin
SERVO_PIN1 = 12
SERVO_MIN_US = 500      # yaklaşık 0°
SERVO_MAX_US = 2500     # yaklaşık 180°

def angle_to_pulse(angle):
    angle = max(0, min(180, angle))
    return SERVO_MIN_US + (SERVO_MAX_US - SERVO_MIN_US) * (angle / 180.0)

pi = pigpio.pi()

pi.set_mode(SERVO_PIN1, pigpio.OUTPUT)

if not pi.connected:
    raise RuntimeError("pigpio daemon çalışmıyor: sudo systemctl start pigpiod")

try:
    while True:
        angle = int(input("Enter angle (0 to 180): "))
        pi.set_servo_pulsewidth(SERVO_PIN, angle_to_pulse(angle))
        angle1 = int(input("Enter angle 1 (0 to 180): "))
        pi.set_servo_pulsewidth(SERVO_PIN1, angle_to_pulse(angle1))
        
        time.sleep(0.3)

except KeyboardInterrupt:
    print("Durduruldu.")

finally:
    pi.set_servo_pulsewidth(SERVO_PIN, 0)
    pi.stop()
