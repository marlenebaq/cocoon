#!/usr/bin/env python

# from picamera.array import PiRGBArray
# from picamera import PiCamera
import time
import argparse as ap
import cv2
import io
import os
import numpy as np

def run():
    resolution = (800, 480)
#    framerate = 35
    framerate = 60

    # Create the VideoCapture object
    cam = cv2.VideoCapture(0)
    # cam = PiCamera()
    # cam.resolution = resolution
    # cam.framerate = framerate
    # raw_capture = PiRGBArray(cam, size=resolution)
    # time.sleep(0.1)

    # If Camera Device is not opened, exit the program
    # if not cam.isOpened():
    #     print "Video device or file couldn't be opened"
    #     exit()

    # stream = cam.capture_continuous(raw_capture, format="bgr", use_video_port=True)

    print time.time()
    print "Stream begun"

    print "Opened window"
    cv2.namedWindow("Image", cv2.WND_PROP_FULLSCREEN)
    cv2.setWindowProperty("Image", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
    while True:
        # print("c")
        retval, img = cam.read()
        # new_img = np.copy(img)
        # raw_capture.truncate(0)

        if cv2.waitKey(10) == ord('p'):
            break
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        for filename in os.listdir("classifiers"):
            if not filename.endswith("xml"):
                print "File not xml, skipping '" + filename + "'"
                continue
            logo_cascade = cv2.CascadeClassifier("classifiers/" + filename)
            logos = logo_cascade.detectMultiScale(gray,
                                                scaleFactor=1.1,
                                                minNeighbors=3,
                                                minSize=(100, 100)
            )
            # Draw a rectangle around the logos
            for (x, y, w, h) in logos:
                logo = img[y:y+h, x:x+w]
                logo = cv2.boxFilter(logo, -1, (30,30))
                img[y:y+logo.shape[0], x:x+logo.shape[1]] = logo

        # window showing cam
        cv2.imshow("Image", img)
    print "Exiting"
    cv2.destroyWindow("Image")
    print "Destroyed window"

if __name__ == "__main__":
    # Parse command line arguments
    # parser = ap.ArgumentParser()
    # group = parser.add_mutually_exclusive_group(required=True)
    # group.add_argument('-d', "--deviceID", help="Device ID")
    # group.add_argument('-v', "--videoFile", help="Path to Video File")
    # parser.add_argument('-l', "--dispLoc", dest="dispLoc", action="store_true")
    # args = vars(parser.parse_args())

    # Get the source of video
    #source = int(args["deviceID"])
    run()
