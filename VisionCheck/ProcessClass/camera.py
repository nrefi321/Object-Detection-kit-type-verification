import cv2 as cv
import numpy as np
import time

class Camera:
    def __init__(self):
        self.source = 1
        self.camConnected = False

    def connection(self):
        try:
            # self.cam = cv.VideoCapture(self.source,cv.CAP_FFMPEG)
            self.cam = cv.VideoCapture(self.source)
            self.camConnected = True
        except Exception as ex:
            print(ex)
            self.camConnected = False
        return self.camConnected

    def setResolution(self,w,h):
        self.cam.set(cv.CAP_PROP_FRAME_WIDTH, w)
        self.cam.set(cv.CAP_PROP_FRAME_HEIGHT, h)

    def disconnect(self):
        if(self.camConnected):
            self.cam.release()

    def delay(self,delay,keys):
        if(self.camConnected):
            return (cv.waitKey(1) & 0xFF == ord(keys))
        return False
       
    def grabImg(self):
        if(self.camConnected):
            return self.cam.read()
        return False,[]   

if __name__ == '__main__':
    cam = Camera()
    cam.connection()
    cam.setResolution(1920,1080)
    if(cam.camConnected):
        previous = time.time()
        currentframe = 0
        while True:
            current = time.time()
            status,img = cam.grabImg()
            if(not status):
                break
            cv.imshow('frame_bgr',img)
            # cv.waitKey(0)
            # if current - previous >= 0.1:
            #     cv.imshow('frame every 100 ms',img)
            #     previous = current
            if(cam.delay(1,'q')):
                break
        cam.disconnect()
        cv.destroyAllWindows()

