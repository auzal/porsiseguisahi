import RPi.GPIO as GPIO
from time import sleep
import argparse
import math
from pythonosc import dispatcher
from pythonosc import osc_server

#GPIO.setmode(GPIO.BOARD)
  # or
GPIO.setmode(GPIO.BCM)

GPIO.setup(12, GPIO.OUT)

similarity = 0

def heart_handler(unused_addr, args, sim):
    similarity = sim
    print(sim)
    
def print_volume_handler(unused_addr, args, volume):
  # print("[{0}] ~ {1}".format(args[0], volume))
  print("{} {}".format(args[0], volume))

def print_compute_handler(unused_addr, args, volume):
  try:
    print("[{0}] ~ {1}".format(args[0], args[1](volume)))
  except ValueError: pass

if __name__ == "__main__":
  parser = argparse.ArgumentParser()
  parser.add_argument("--ip",
      default="127.0.0.1", help="The ip to listen on")
  parser.add_argument("--port",
      type=int, default=5005, help="The port to listen on")
  args = parser.parse_args()

  dispatcher = dispatcher.Dispatcher()
  dispatcher.map("/heart", heart_handler, "Heart")
  dispatcher.map("/volume", print_volume_handler, "Volume")
  dispatcher.map("/logvolume", print_compute_handler, "Log volume", math.log)

  server = osc_server.ThreadingOSCUDPServer(
      (args.ip, args.port), dispatcher)
  print("Serving on {}".format(server.server_address))
  
  server.serve_forever()
  while True:
    print("hello")
    GPIO.output(12, 1)
    sleep(.09)
    GPIO.output(12, 0)
    sleep(.2)
    GPIO.output(12, 1)
    sleep(.09)
    GPIO.output(12, 0)
    heart_val = 1-similarity;
    sleep((.6 *similarity)+.3)


  GPIO.cleanup()
