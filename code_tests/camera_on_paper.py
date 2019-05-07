from picamera import PiCamera
from time import sleep
from papirus import PapirusImage
#from papirus import Papirus

image = PapirusImage(0)


camera = PiCamera()
camera.start_preview(fullscreen=False, window=(100,100,640,480))


while True:
    camera.capture('/home/pi/Desktop/image.jpg')
    image.write('/home/pi/Desktop/image.jpg')
    #image.partial_update()
    #sleep(2)
    #camera.stop_preview()
