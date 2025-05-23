
import time

from ast import While
import cv2 as cv
import time
import pyautogui
import numpy as np


class Screenshot:
    def __init__(self):
        # self.source = 'D:\project_Fern\VR20\VR20_proc\camera\VR20.mp4'
        self.scr = None
        self.scrConnected = False

    def start_screenshot(self):
        try:
            self.scr = pyautogui.screenshot()
            self.scrConnected = True
        except Exception as ex:
            print(ex)
            self.scrConnected = False
        return self.scrConnected

    def disconnect(self):
        if (self.start_screenshot()):
            self.scr.release()

    def delay(self, delay, keys):
        if (self.start_screenshot()):
            return (cv.waitKey(1) & 0xFF == ord(keys))
        return False

    def grabImg(self):
        if (self.scrConnected):
            img = np.array(self.scr)
            img = cv.cvtColor(np.asarray(img), cv.COLOR_RGB2BGR)
            return img
        return False

if __name__ == '__main__':
    cam = Screenshot()
    cam.start_screenshot()
    if (cam.start_screenshot()):
        previous = time.time()
        currentframe = 0
        while True:
            current = time.time()
            img = cam.grabImg()
            img = cv.cvtColor(img, cv.COLOR_BGR2RGB)
            # status, img = cam.grabImg()
            # if (not status):
            #     break
            cv.imshow('frame_bgr', img)
            # if current - previous >= 0.1:
            #     cv.imshow('frame every 100 ms',img)
            #     previous = current
            if (cam.delay(1, 'q')):
                break
        cam.disconnect()
        cv.destroyAllWindows()
