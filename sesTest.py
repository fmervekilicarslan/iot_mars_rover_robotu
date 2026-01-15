import RPi.GPIO as GPIO
import time

# Set up GPIO pin numbering mode and the sound sensor pin
GPIO.setmode(GPIO.BCM)
SOUND_SENSOR_PIN = 4  # GPIO pin number (adjust as needed)
GPIO.setup(SOUND_SENSOR_PIN, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

# Function to check and print sound detection status
def detect_sound():
    sound_detected = GPIO.input(SOUND_SENSOR_PIN)  # Read the digital signal

    # The KY-037 module has a potentiometer (small screw-like component) that adjusts the sensitivity.
    # Tuning this potentiometer is crucial to get accurate readings. Turning it clockwise increases sensitivity,
    # which means the sensor will detect lower sound levels and produce more "1" (sound detected) outputs.
    # Turning it counter-clockwise decreases sensitivity, making it less likely to detect sound (producing more "0" outputs).
    # If the sensor is only showing "1" (sound detected) values, rotate the potentiometer counter-clockwise
    # (you may need to rotate it up to 100 times) until you start seeing "0" values. This adjustment sets the sensitivity threshold
    # so that it can correctly detect and respond to sound changes.

    if sound_detected == 1:
        print("Sound detected!")  # Sound detected
    else:
        print("No sound detected.")  # No sound detected

# Main program loop
try:
    print("Tuning your KY-037 sound sensor: Adjust the potentiometer to get accurate 0/1 readings.")
    print("If you see only 'Sound detected!' messages, reduce sensitivity by rotating the screw counter-clockwise.")
    while True:
        detect_sound()  # Check sound sensor status
except KeyboardInterrupt:
    print("Program interrupted. Cleaning up GPIO settings.")
    GPIO.cleanup()  # Clean up all GPIO settings
