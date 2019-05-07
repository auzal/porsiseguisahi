import RPi.GPIO as GPIO
from time import sleep

#GPIO.setmode(GPIO.BOARD)
  # or
GPIO.setmode(GPIO.BCM)

GPIO.setup(12, GPIO.OUT)


while True:

    GPIO.output(12, 1)
    sleep(.09)
    GPIO.output(12, 0)
    sleep(.2)
    GPIO.output(12, 1)
    sleep(.09)
    GPIO.output(12, 0)
    sleep(.6)


GPIO.cleanup()
