#import opencv
from fps import FPS
import cv2
import numpy as np
from threading import Thread
import time
import imutils
import os


WINDOW_WIDTH = 640
WINDOW_HEIGHT = 480
#make two separate threads. One for the imshow and one for the webcam
class WebcamVideoStream:
    def __init__(self, src=0):
        # initialize the video camera stream and read the first frame
        # from the stream
        self.stream = cv2.VideoCapture(src)\

        print("Camera Width: " + str(self.stream.get(3)))
        print("Camera Height: " + str(self.stream.get(4)))
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

        #see if output.mp4 exists, if it does, increase the number by 1
        #this is to prevent overwriting the file
        i = 1
        while True:
            if os.path.exists("output" + str(i) + ".avi"):
                i += 1
            else:
                break
        #create the video writer
      #self.out = cv2.VideoWriter('output' + str(i) + '.avi', cv2.VideoWriter_fourcc(*'XVID'), 20.0, (WINDOW_WIDTH, WINDOW_HEIGHT))
            #out = cv2.VideoWriter('outpy.avi',cv2.VideoWriter_fourcc('M','J','P','G'), 10, (frame_width,frame_height))
        self.out = cv2.VideoWriter('output'+ str(i) +'.avi', cv2.VideoWriter_fourcc('M','J','P','G'), 30.0, (WINDOW_WIDTH, WINDOW_HEIGHT))

    def start(self):
        Thread(target=self.update, args=()).start()
        return self

    def update(self):
        global invert
        invert = False
        while True:
            if self.stopped:
                return
            frame = self.stream.read()
            frame = cv2.resize(frame, (WINDOW_WIDTH, WINDOW_HEIGHT))
            self.fps.update()
            self.fps.stop()
            cv2.putText(frame, "FPS: {:.2f}".format(self.fps.fps()), (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 0, 0), 2)
            # Night Vision Effect ( SIMULATED )
            # convert to grayscale
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            # invert the grayscale image
            if invert:
                frame = 255 - gray
                
            cv2.imshow("Night Vision", frame)
            
            #write video to output.avi
            #self.out.write(frame)
            cv2.waitKey(1)

    def stop(self):
        self.stopped = True
        self.stream.stop()
        self.out.release()



if __name__ == '__main__':
    window = ShowVideo()
    window.start()


    while True:

        command = input("Enter a command: ")
        if command == "invert":
            invert = True
        elif command == "normal":
            invert = False
        elif command == "exit":
            window.stop()

            break
        else:
            print("Invalid command")
    
    cv2.destroyAllWindows()

        