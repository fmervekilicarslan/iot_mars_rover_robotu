import pigpio
import time

#servo pinler
SERVO_PIN1 = 23          # BCM pin
SERVO_PIN2 = 24
SERVO_PIN3 = 25
SERVO_PIN4 = 17
SERVO_MIN_US = 500      # yaklaşık 0°
SERVO_MAX_US = 2500     # yaklaşık 180°

#bts7960 pinler (1 sag bts; 2 sol bts)
RPWM1 = 26
LPWM1 = 20
RPWM2 = 15
LPWM2 = 18


#servo aci
def angle_to_pulse(angle):
    angle = max(0, min(180, angle))
    return SERVO_MIN_US + (SERVO_MAX_US - SERVO_MIN_US) * (angle / 180.0)

pi = pigpio.pi()

#servo
pi.set_mode(SERVO_PIN3, pigpio.OUTPUT)
pi.set_mode(SERVO_PIN4, pigpio.OUTPUT)

#bts7960
pi.set_mode(RPWM1, pigpio.OUTPUT)
pi.set_mode(LPWM1, pigpio.OUTPUT)
pi.set_mode(RPWM2, pigpio.OUTPUT)
pi.set_mode(LPWM2, pigpio.OUTPUT)

#bts7960 yon
def right(speed):
    # speed: 0–255
    print("sag")
    pi.set_PWM_dutycycle(RPWM1, speed)
    pi.set_PWM_dutycycle(LPWM1, 0)
    pi.set_PWM_dutycycle(RPWM2, speed)
    pi.set_PWM_dutycycle(LPWM2, 0)

def left(speed):
    print("sol")
    pi.set_PWM_dutycycle(RPWM1, 0)
    pi.set_PWM_dutycycle(LPWM1, speed)
    pi.set_PWM_dutycycle(RPWM2, 0)
    pi.set_PWM_dutycycle(LPWM2, speed)
    
def reverse(speed):
    print("geri")
    pi.set_PWM_dutycycle(RPWM1, speed)
    pi.set_PWM_dutycycle(LPWM1, 0)
    pi.set_PWM_dutycycle(RPWM2, 0)
    pi.set_PWM_dutycycle(LPWM2, speed)

def forward(speed):
    print("ileri")
    pi.set_PWM_dutycycle(RPWM1, 0)
    pi.set_PWM_dutycycle(LPWM1, speed)
    pi.set_PWM_dutycycle(RPWM2, speed)
    pi.set_PWM_dutycycle(LPWM2, 0)
        
def stop():
    print("durma")
    pi.set_PWM_dutycycle(RPWM1, 0)
    pi.set_PWM_dutycycle(LPWM1, 0)
    pi.set_PWM_dutycycle(RPWM2, 0)
    pi.set_PWM_dutycycle(LPWM2, 0)
    
if not pi.connected:
    raise RuntimeError("pigpio daemon çalışmıyor: sudo systemctl start pigpiod")

try:
    
    forward(150)
    time.sleep(2)
    left(175)
    time.sleep(2)
    stop()    
    
    #while True:
        #angle = int(input("Enter angle (0 to 180): "))
        #pi.set_servo_pulsewidth(SERVO_PIN3, angle_to_pulse(angle))
        #angle1 = int(input("Enter angle 1 (0 to 180): "))
        #pi.set_servo_pulsewidth(SERVO_PIN3, angle_to_pulse(angle1))
        
        #time.sleep(0.3)       
        
    

except KeyboardInterrupt:
    print("Durduruldu.")

finally:
    pi.set_servo_pulsewidth(SERVO_PIN1, 0)
    pi.set_servo_pulsewidth(SERVO_PIN2, 0)
    pi.set_servo_pulsewidth(SERVO_PIN3, 0)
    pi.set_servo_pulsewidth(SERVO_PIN4, 0)
    pi.stop()
