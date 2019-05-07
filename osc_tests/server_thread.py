"""Small example OSC server

This program listens to several addresses, and prints some information about
received packets.
"""
import argparse
import math
from threading import Thread
from time import sleep

from pythonosc import dispatcher
from pythonosc import osc_server

import RPi.GPIO as GPIO
from time import sleep

GPIO.setmode(GPIO.BCM)

GPIO.setup(12, GPIO.OUT)


similarity = 0

def heart_handler(unused_addr, args, sim):
 # print(args[0])
 # print(sim)
  global similarity 
  similarity = sim
  print(similarity)

def print_volume_handler(unused_addr, args, volume):
  print("[{0}] ~ {1}".format(args[0], volume))

def print_compute_handler(unused_addr, args, volume):
  try:
    print("[{0}] ~ {1}".format(args[0], args[1](volume)))
  except ValueError: pass

def beat():
  while True:
    factor = 1 - similarity
    GPIO.output(12, 1)
    sleep(.09)
    GPIO.output(12, 0)
    sleep(.2)
    GPIO.output(12, 1)
    sleep(.09)
    GPIO.output(12, 0)
    sleep(1 * factor + .2)

thread = Thread(target=beat)
thread.start()

parser = argparse.ArgumentParser()
parser.add_argument("--ip",  default="127.0.0.1", help="The ip to listen on")
parser.add_argument("--port", type=int, default=5005, help="The port to listen on")
args = parser.parse_args()
dispatcher = dispatcher.Dispatcher()
dispatcher.map("/heart", heart_handler, "Sim")
dispatcher.map("/volume", print_volume_handler, "Volume")
dispatcher.map("/logvolume", print_compute_handler, "Log volume", math.log)
server = osc_server.ThreadingOSCUDPServer((args.ip, args.port), dispatcher)
print("Serving on {}".format(server.server_address))
server.serve_forever()


##GPIO.cleanup()



  
