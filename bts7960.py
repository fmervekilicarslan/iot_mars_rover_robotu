import RPi.GPIO as GPIO
import time

RPWM = 18
LPWM = 23

GPIO.setmode(GPIO.BCM)
GPIO.setup(RPWM, GPIO.OUT)
GPIO.setup(LPWM, GPIO.OUT)

GPIO.output(RPWM,1)
GPIO.output(LPWM,0)
time.sleep(2)


GPIO.cleanup()
