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
from papirus import PapirusImage

papirus = PapirusImage(270)

# Get a reference to the Raspberry Pi camera.
# If this fails, make sure you have a camera connected to the RPi and that you
# enabled your camera in raspi-config and rebooted first.
camera = picamera.PiCamera()
camera.resolution = (320, 240)
output = np.empty((240, 320, 3), dtype=np.uint8)

# Load a sample picture and learn how to recognize it.
print("Loading known face image(s)")
obama_image = face_recognition.load_image_file("obama_small.jpg")
obama_face_encoding = face_recognition.face_encodings(obama_image)[0]

# Initialize some variables
face_locations = []
face_encodings = []

face_counter = 0

while True:
    print("Capturing image.")
    # Grab a single frame of video from the RPi camera as a numpy array
    camera.capture(output, format="rgb")

    # Find all the faces and face encodings in the current frame of video
    face_locations = face_recognition.face_locations(output)

    for face_location in face_locations:

        # Print the location of each face in this image
        top, right, bottom, left = face_location
        print("A face is located at pixel location Top: {}, Left: {}, Bottom: {}, Right: {}".format(top, left, bottom, right))

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
        
        pil_image.save(str(face_counter ) + '.JPEG',"JPEG")
      
        papirus.write('/home/pi/Desktop/' + str(face_counter) + '.JPEG')
      #  face_counter += 1
    
    
##    print("Found {} faces in image.".format(len(face_locations)))
##    face_encodings = face_recognition.face_encodings(output, face_locations)
##
##    # Loop over each face found in the frame to see if it's someone we know.
##    for face_encoding in face_encodings:
##        # See if the face is a match for the known face(s)
##        match = face_recognition.compare_faces([obama_face_encoding], face_encoding)
##        name = "<Unknown Person>"
##
##        if match[0]
##            name = "Barack Obama"
##
##        print("I see someone named {}!".format(name))
