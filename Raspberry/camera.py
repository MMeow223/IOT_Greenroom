import cv2 as cv
import uuid
import datetime
import os
from dotenv import load_dotenv

load_dotenv()


def capture_image():

    filename = '{0}/{1}-{2}.png'.format(os.getenv("IMAGE_FOLDER"), str(datetime.datetime.now().date()),
                                        str(uuid.uuid4()))

    print(filename)
    try:
        cam = cv.VideoCapture(0)

        ret, frame = cam.read()

        if not ret:
            print("error in retrieving frame")
            return False

        img = cv.cvtColor(frame, cv.COLOR_BGRA2BGR)
        cv.imwrite(filename, img)
        cam.release()
        return filename

    except Exception as e:
        print("error opening camera")
        print(e)
        return False


capture_image()
