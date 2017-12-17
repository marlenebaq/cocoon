import argparse as ap
import cv2
import os

def run(source):
    # Create the VideoCapture object
    cam = cv2.VideoCapture(source)

    # If Camera Device is not opened, exit the program
    if not cam.isOpened():
        print "Video device or file couldn't be opened"
        exit()

    print "Press key `p` to pause the video to start tracking"
    cv2.namedWindow("Image", cv2.WND_PROP_FULLSCREEN)
    cv2.setWindowProperty("Image",cv2.WND_PROP_FULLSCREEN,cv2.WINDOW_FULLSCREEN)
    while True:
        # Retrieve an image and Display it.
        retval, img = cam.read()
        if not retval:
            print "Cannot capture frame device"
            exit()
        
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
                # cv2.rectangle(img, (x, y), (x+w, y+h), (0, 255, 0), 2)
                logo = img[y:y+h, x:x+w]
                logo = cv2.boxFilter(logo, -1, (30,30))
                img[y:y+logo.shape[0], x:x+logo.shape[1]] = logo

        # window showing cam
        # print "window"
        cv2.imshow("Image", img)
        # print "window done"
    cv2.destroyWindow("Image")

if __name__ == "__main__":
    # Parse command line arguments
    parser = ap.ArgumentParser()
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('-d', "--deviceID", help="Device ID")
    # group.add_argument('-v', "--videoFile", help="Path to Video File")
    # parser.add_argument('-l', "--dispLoc", dest="dispLoc", action="store_true")
    args = vars(parser.parse_args())

    # Get the source of video
    source = int(args["deviceID"])
    run(source)
