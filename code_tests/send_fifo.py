import os, stat
import random
import sys

path = "/tmp/my_program.fifo"

try:
  if stat.S_ISFIFO(os.stat(path).st_mode):
    print('exists')
    os.unlink(path)
except:
  pass

print("mkfifo")
sys.stdout.flush()
os.mkfifo(path)

print("open")
sys.stdout.flush()
fifo = open(path, "w")

print("while")
sys.stdout.flush()

while True:
  print("hello")
  sys.stdout.flush()
  fifo.write("{}\n".format(0))

fifo.close()
