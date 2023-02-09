#import opencv
from fps import FPS
import cv2
import numpy as np
from threading import Thread
import time
import imutils
import os
import sys

WINDOW_WIDTH = 500
WINDOW_HEIGHT = 500
WINDOW_SCALE_FACTOR = 1.0
command = ""
record = False 

#make two separate threads. One for the imshow and one for the webcam
class WebcamVideoStream:
    def __init__(self, src=0):
        global WINDOW_WIDTH
        global WINDOW_HEIGHT
        global WINDOW_SCALE_FACTOR
        # initialize the video camera stream and read the first frame
        # from the stream
        self.stream = cv2.VideoCapture(src)

        print("Camera Width: " + str(self.stream.get(3)))
        print("Camera Height: " + str(self.stream.get(4)))

        CAMERA_WIDTH = self.stream.get(3)
        CAMERA_HEIGHT = self.stream.get(4)

        #resize window width and height to be same ratio as camera width and height
        WINDOW_WIDTH = int(CAMERA_WIDTH * (WINDOW_HEIGHT / CAMERA_HEIGHT))
        WINDOW_HEIGHT = int(CAMERA_HEIGHT * (WINDOW_WIDTH / CAMERA_WIDTH))

        WINDOW_HEIGHT = int(WINDOW_HEIGHT * WINDOW_SCALE_FACTOR)
        WINDOW_WIDTH = int(WINDOW_WIDTH * WINDOW_SCALE_FACTOR)

        print("Window Width: " + str(WINDOW_WIDTH))
        print("Window Height: " + str(WINDOW_HEIGHT))

        print("Camera FPS: " + str(self.stream.get(5)))
        print("Camera Brightness: " + str(self.stream.get(10)))

        (self.grabbed, self.frame) = self.stream.read()
        # initialize the variable used to indicate if the thread should
        # be stopped
        self.stopped = False

    def start(self):
        # start the thread to read frames from the video stream
        Thread(target=self.update, args=()).start()
        return self

    def update(self):
        # keep looping infinitely until the thread is stopped
        while True:
            # if the thread indicator variable is set, stop the thread
            if self.stopped:
                return

            # otherwise, read the next frame from the stream
            (self.grabbed, self.frame) = self.stream.read()

    def read(self):
        # return the frame most recently read
        return self.frame

    def stop(self):
        # indicate that the thread should be stopped
        self.stopped = True


# imshow thread
class ShowVideo:
    def __init__(self, src=0):
        self.stream = WebcamVideoStream(src).start()
        self.fps = FPS().start()
        self.stopped = False

    def start(self):
        #Thread(target=self.update, args=()).start()
        #set fullscreen

        #waitkey thread
        cv2.namedWindow("Night Vision", cv2.WND_PROP_FULLSCREEN)        
        self.update()
        return self


    def update(self):
        global invert
        global record
        global command

        invert = False
        while True:
            if self.stopped:
                return
            frame = self.stream.read()
            frame = cv2.resize(frame, (WINDOW_WIDTH, WINDOW_HEIGHT))
            #frame = imutils.resize(frame, width=WINDOW_WIDTH)
            self.fps.update()
            self.fps.stop()
            cv2.putText(frame, "FPS: {:.2f}".format(self.fps.fps()), (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 0, 0), 2)
            #crosshair using this pseuodocode line((screenWidth/2)-20, screenHeight/2, (screenWidth/2)+20, screenHeight/2);  line(screenWidth/2, (screenHeight/2)-20, screenWidth/2, (screenHeight/2)+20); 
            cv2.line(frame, (int(WINDOW_WIDTH/2)-20, int(WINDOW_HEIGHT/2)), (int(WINDOW_WIDTH/2)+20, int(WINDOW_HEIGHT/2)), (255, 0, 0), 1)
            cv2.line(frame, (int(WINDOW_WIDTH/2), int(WINDOW_HEIGHT/2)-20), (int(WINDOW_WIDTH/2), int(WINDOW_HEIGHT/2)+20), (255, 0, 0), 1)

            
            # Night Vision Effect ( SIMULATED )
            # convert to grayscale            # invert the grayscale image
            if invert:
                frame = 255 - frame
                
            cv2.imshow("Night Vision", frame)
            
            key = cv2.waitKey(1) & 0xFF
            if key == ord("q"):
                command = "exit"
            elif key == ord("r"):
                self.start_video()
            elif key == ord("s"):
                self.stop_video()
            elif key == ord("i"):
                invert = True
            elif key == ord("n"):
                invert = False
                

            #write video to output.avi
            if record:
                self.out.write(frame)

    def stop(self):
        global record
        self.stopped = True
        self.stream.stop()
        if record and self.out.isOpened():
            self.out.release()

    def start_video(self):
        global record
        if not record:
            i = 1
            while True:
                if os.path.exists("output" + str(i) + ".avi"):
                    i += 1
                else:
                    break
            
            self.out = cv2.VideoWriter('output'+ str(i) +'.avi', cv2.VideoWriter_fourcc('M','J','P','G'), 30.0, (WINDOW_WIDTH, WINDOW_HEIGHT))
            record = True

    def stop_video(self):
        global record
        if record and self.out.isOpened():
            self.out.release()
            record = False

def commandListener():
    global record
    global command
    while True:
        if command == "invert":
            invert = True
        elif command == "normal":
            invert = False
        elif command == "exit":
            break
        elif command == "record":
            record = True
        elif command == "save":
            window.stop_video()
        elif command == "":
            pass
        else:
            print("Invalid command")
        time.sleep(0.5)
    try:
        window.stop()
        exit()
    except:
        pass
    
   


if __name__ == '__main__':
    window = ShowVideo()
    t1 = Thread(target=commandListener).start()

    window.start()


   

        
    
    
   