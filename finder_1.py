# This is a demo of running face recognition on a Raspberry Pi.
# This program will print out the names of anyone it recognizes to the console.

# To run this, you need a Raspberry Pi 2 (or greater) with face_recognition and
# the picamera[array] module installed.
# You can follow this installation instructions to get your RPi set up:
# https://gist.github.com/ageitgey/1ac8dbe8572f3f533df6269dab35df65

import face_recognition
import picamera
import numpy as np
from PIL import Image
from time import sleep
from papirus_mod import PapirusImage

import argparse
import random
import time
from glob import glob

from pythonosc import osc_message_builder
from pythonosc import udp_client

papirus = PapirusImage(270)

# Get a reference to the Raspberry Pi camera.
# If this fails, make sure you have a camera connected to the RPi and that you
# enabled your camera in raspi-config and rebooted first.
camera = picamera.PiCamera()
camera.resolution = (320, 240)
output = np.empty((240, 320, 3), dtype=np.uint8)

cam_h = 240
cam_w = 320

# Load a sample picture and learn how to recognize it.
ariel_encodings = []
fabi_encodings = []

print("Loading known face image(s)")
for image_name in glob("ref_photos/*jpg"):
    #import pdb; pdb.set_trace()
    print(image_name)
    if(image_name.split("/")[1][0]=='a'):
        ariel_image = face_recognition.load_image_file(image_name)
        ariel_encodings.append(face_recognition.face_encodings(ariel_image)[0])
    if(image_name.split("/")[1][0]=='f'):
        fabi_image = face_recognition.load_image_file(image_name)
        fabi_encodings.append(face_recognition.face_encodings(fabi_image)[0])

print("encoding lengths.")

print(len(ariel_encodings))
print(len(fabi_encodings))

# Initialize some variables
face_locations = []
face_encodings = []

face_counter = 0

similarity = 0.5

parser = argparse.ArgumentParser()
parser.add_argument("--ip", default="127.0.0.1",
      help="The ip of the OSC server")
parser.add_argument("--port", type=int, default=5005,
      help="The port the OSC server is listening on")
args = parser.parse_args()

client = udp_client.SimpleUDPClient(args.ip, args.port)




while True:
    print("Capturing image.")
    # Grab a single frame of video from the RPi camera as a numpy array
    camera.capture(output, format="rgb")
   # import pdb; pdb.set_trace()

    # Find all the faces and face encodings in the current frame of video
    face_locations = face_recognition.face_locations(output)

    if len(face_locations)>0:
        face_location = face_locations[0]
        face_encodings = face_recognition.face_encodings(output, face_locations)[0]
        # Print the location of each face in this image
        top, right, bottom, left = face_location

        image_w = right-left
        image_h = bottom-top
        
        print("A face is located at pixel location Top: {}, Left: {}, Bottom: {}, Right: {}".format(top, left, bottom, right))
        margin =.2 
        top -= int(margin * 2 * image_h)
        top = max(top,0)
        bottom += int(margin *2 * image_h)
        bottom = min(bottom,cam_h)
        left -= int(margin * image_w)
        left = max(0,left)
        right += int(margin * image_w)
        right = min(right,cam_w)

        # You can access the actual face itself like this:
        face_image = output[top:bottom, left:right]
        pil_image = Image.fromarray(face_image)
        #pil_image.show()
        # NOTE -> display resolution is documented in adafruit as 2" 200 x 96
        # and in the official documentation as 1.44" 196 X 96
        # shitty documentation. I'm asuming adafruit is right

        w,h = pil_image.size

        #print(str(w) + ", " + str(h))

        new_w = int(96)

        new_h = int(h*96/w)

        pil_image = pil_image.resize((new_w,new_h))
        
       # pil_image.save(str(face_counter ) + '.JPEG',"JPEG")
      
        papirus.writeCool(pil_image)

        ariel_sim_scores = face_recognition.face_distance(ariel_encodings, face_encodings)
       # print(ariel_sim_score)
        ariel_score = min(ariel_sim_scores)

        fabi_sim_scores = face_recognition.face_distance(fabi_encodings, face_encodings)
       # print(ariel_sim_score)
        fabi_score = min(ariel_sim_scores)

        
        similarity = fabi_score*.75 + ariel_score*.25
      #  similarity = ariel_score
        print(similarity)
        client.send_message("/heart", similarity)


        
        
        
##        print("Found {} faces in image.".format(len(face_locations)))
##        face_encodings = face_recognition.face_encodings(output, face_locations)
##    
##        # Loop over each face found in the frame to see if it's someone we know.
##        for face_encoding in face_encodings:
##            # See if the face is a match for the known face(s)
##            match = face_recognition.compare_faces([obama_face_encoding], face_encoding)
##            name = "<Unknown Person>"
##    
##            if match[0]
##                name = "Barack Obama"
##    
##            print("I see someone named {}!".format(name))


