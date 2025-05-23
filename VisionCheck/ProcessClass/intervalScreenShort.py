import cv2 as cv
import numpy as np
from sqlalchemy import false, true
# from ProcessClass.repeatedTimer import RepeatedTimer
from repeatedTimer import RepeatedTimer
from camera import Camera
import mss

# import Jetson.GPIO as GPIO

class IntervalScreenshot:
    def __init__(self,monitor = 1,useInterval = False,interval = None,callback = None):
        self.cam = Camera()
        self.monitor = monitor
        self.interval = 1 #second
        if(interval is not None):
            self.interval = interval

        self.useInterval = useInterval
        
        self.callbacks = None
        if(callback is not None):
            self.subscribe(callback)
        self.flagStartStop = False
        
        self.timer = RepeatedTimer(self.interval,self.testinput(true,true))
        if(self.useInterval):
            self.flagStartStop = True
            self.timer.start()

    def subscribe(self, callback):
        self.callbacks = callback

    def publish(self,img):
        self.callbacks(img)
    
    # def GPIOInput(self,hardwareConnect=False,start_loop_gpio=False):
    #     if(hardwareConnect):
    #         GPIO.setmode(GPIO.BOARD) 
    #         GPIO.setup(7, GPIO.IN)
    #         GPIO.setup(13,GPIO.IN)
    #         GPIO.setup(15,GPIO.IN)
    #         GPIO.setup(29,GPIO.IN)
    #         while start_loop_gpio:
    #             IO1 = GPIO.input(7)
    #             IO2 = GPIO.input(13)
    #             IO3 = GPIO.input(15)
    #             IO4 = GPIO.input(29)
    #             if IO1 == GPIO.HIGH:
    #                 return True
    #             elif IO2 == GPIO.HIGH:
    #                 return True
    #             elif IO3 == GPIO.HIGH:
    #                 return True
    #             elif IO4 == GPIO.HIGH:
    #                 return True
    #             else:
    #                 return False
    
    def testinput(self,hardwareConnect,start_loop_gpio):
        if(hardwareConnect):
            print("connect hardware")
            high = "HIGH"
            low = "LOW"
            while start_loop_gpio:
                print("Input:")
                inputdata = input()
                print(inputdata)
                if inputdata == high:
                    return True
                elif inputdata == low:
                    return False
                else:
                    return False

    def camera(self):
        pass




    def screenshort(self):
        #scn = pyautogui.screenshot()
        #img = np.array(scn)
        #img = cv.cvtColor(np.asarray(img), cv.COLOR_RGB2BGR)
        with mss.mss() as sct:
            monitor = sct.monitors[self.monitor]  # or a region
            scn = sct.grab(monitor)
        img = np.array(scn)
        img = cv.cvtColor(img, cv.COLOR_BGRA2BGR)
        if(self.flagStartStop):
            self.publish(img)
        return img

    def stopInterval(self):
        self.flagStartStop = False
        self.timer.stop()
    
    def startInterval(self,interval = 1):
        self.interval = interval
        self.flagStartStop = True
        self.timer.interval = self.interval
        self.timer.start()

i = 0
def testFunction(img):
    global i
    dimension = img.shape
    height = img.shape[0]
    width = img.shape[1]
    chanel = img.shape[2]
    print('Image Dimension    : ',dimension)
    print('Image Height       : ',height)
    print('Image Width        : ',width)
    print('Number Of Chanel   : ',chanel)
    #cv.imshow('Test',cv.resize(img,(640,480)))
    #cv.imwrite('D:/vr20/{}-lossy.png'.format(i),img)
    # cv.imwrite('D:/vr20/{}-lossless.png'.format(i),img, [cv.IMWRITE_PNG_COMPRESSION, 0])
    i+=1
    
if __name__ == '__main__':
    # scn = IntervalScreenshot(1,True,3,testFunction)
    scn = IntervalScreenshot(1,True,3,)
    try:
        a = input()    
    except:
        pass
    scn.stopInterval()
    #test Pass
