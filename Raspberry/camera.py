# from picamera import PiCamera
# from time import sleep
# import datetime
# camera = PiCamera()

# camera.start_preview(alpha=200)
# sleep(5)
# camera.stop_preview()

# def capture_image():
#     image_filename = datetime.datetime.now().strftime("%Y%m%d%H%M%S") 
#     camera.capture('/home/pi/Desktop/{0}.jpg'.format(image_filename))
    

    
import cv2

cam = cv2.VideoCapture(0)

while True:
    check, frame = cam.read()

    cv2.imshow('video', frame)

    key = cv2.waitKey(1)
    if key == 27:
        break

cam.release()
cv2.destroyAllWindows()