import cv2 
import time
from time import sleep
import imageio
import os
import sys

path = os.path.realpath(
            os.path.join(os.getcwd(), os.path.dirname(__file__)))

logstdout = os.path.join(path, "Logs", "stdout-capture_pyw.txt")
logstderr = os.path.join(path, "Logs", "stderr-capture_pyw.txt")
#if sys.executable.endswith("python.exe"):
sys.stdout = open(logstdout, "w")
sys.stderr = open(logstderr, "w")


#webcam = cv2.VideoCapture(0)
webcam = cv2.VideoCapture(cv2.CAP_DSHOW)
if not webcam.isOpened() or webcam is None:
    print("Could not connect to camera stream")
else:

    # https://stackoverflow.com/questions/11420748/setting-camera-parameters-in-opencv-python
    #webcam.set(6, cv2.VideoWriter.Fourcc('M','J','P','G'))
    print(webcam.set(3, 1920))
    print(webcam.set(4, 1080))
    # print(webcam.set(cv2.CAP_PROP_AUTOFOCUS, False))
    # print(webcam.set(cv2.CAP_PROP_FOCUS, 0))
    # print(webcam.set(cv2.CAP_PROP_EXPOSURE, -5))
    # print(webcam.set(cv2.CAP_PROP_AUTO_EXPOSURE, True))

    #check, frame = webcam.read()
    sleep(1.5)
    check, frame = webcam.read()

    if(check):

        image_folder = os.path.join(path, "Captures", "Captures_Today")

        if not os.path.exists(image_folder):
            os.makedirs(image_folder)

        timestr = os.path.join(image_folder, os.path.join(time.strftime("%Y_%m_%d-%H.%M.%S.jpg")))

        cv2.imwrite(filename=timestr, img=frame)
        webcam.release()