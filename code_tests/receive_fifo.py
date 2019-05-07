import os
import sys
import RPi.GPIO as GPIO
from time import sleep
import sys

#GPIO.setmode(GPIO.BOARD)
  # or
GPIO.setmode(GPIO.BCM)

GPIO.setup(12, GPIO.OUT)

path = "/tmp/my_program.fifo"
fifo = open(path, "r")

similarity = 0

while True:
  read_data = fifo.readline()

  print('read', len(read_data), read_data)
  sys.stdout.flush()

  similarity = 1 - float(read_data.strip())
  print(similarity)
  sys.stdout.flush()

  GPIO.output(12, 1)
  sleep(.09)
  GPIO.output(12, 0)
  sleep(.2)
  GPIO.output(12, 1)
  sleep(.09)
  GPIO.output(12, 0)
  sleep((.8 * similarity)+.2)

GPIO.cleanup()
fifo.close()

