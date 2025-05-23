import Jetson.GPIO as GPIO
import time

class JetsonGPIO:
    def __init__(self):
        self.pin_in = [7,13,15,29] #BCM  = 4,27,22,5
        self.pin_out = [31,33,35,37] #BCM = 6,13,19,26
        self.hardwareConnect = False
        self.initIO()
            
    def initIO(self):
        try:
            GPIO.setmode(GPIO.BOARD)
            for i in range(0,3):
                GPIO.setup(self.pin_in[i], GPIO.IN)
                GPIO.setup(self.pin_out[i],GPIO.OUT)
                self.outputWrite(i)
            self.hardwareConnect = True
        except:
            self.hardwareConnect = False

    def outputWrite(self,ch,on = False):
        if(not self.hardwareConnect):
            return
        if(ch <0 or ch>3):
            return
        if(on):
            GPIO.output(self.pin_out[ch],GPIO.HIGH)
        else:
            GPIO.output(self.pin_out[ch],GPIO.LOW)
        
    def closeIO(self):
        if(self.hardwareConnect):
            GPIO.cleanup()

    def readInput(self,ch):
        # print(f"Pin {self.pin_in[ch]}")
        if(not self.hardwareConnect):
            return None
        if(ch <0 or ch>3):
            return None
        return GPIO.input(self.pin_in[ch])
    
    def readInputDebounce1(self,ch,waittime=0.5):
        # GPIO.add_event_detect(self.pin_in[ch], GPIO.BOTH, callback=io.my_callback,bouncetime=200)  
        IO = self.readInput(ch)
        # print(f"Input {IO} ch {ch}")
        if IO == True:     
            # print(f"state is {IO}")
            time.sleep(waittime)
            return IO
        else:
            # print(f"state is { IO}")
            return IO

    def readInputDebounce(self, ch, waittime=0.05):
        first_read = self.readInput(ch)
        time.sleep(waittime)
        second_read = self.readInput(ch)
        # print(f"first_read {first_read} second_read {second_read} ch {ch}")

        if first_read == second_read:
            return second_read  # Stable value
        else:
            return None  # Unstable or bouncing


    def my_callback(channel):  
        if GPIO.input(7):     # if port 25 == 1  
            print("Rising edge") 
        else:                  # if port 25 != 1  
            print("Falling edge") 

    def GPIOInput1(self):
        # prev_value = None   
        value = None 
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(self.pin_in,GPIO.IN)
        print("start")
        try:
            while True:
                value = GPIO.input(self.pin_in)
                if value != None:
                    if value == GPIO.HIGH:
                        value_str = "HIGH"
                        return True
                    else:
                        value_str = "LOW"
                        return False
                    # print("Read pin {} : {} ".format(self.pin_in,value_str))
                    # prev_value = value
                time.sleep(1)
        finally:
            GPIO.cleanup()

    def GPIOOutput1(self):
        prev_value = None  
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(self.pin_out,GPIO.OUT,initial=GPIO.HIGH)
        print("Start")
        curr_value = GPIO.HIGH
        try:
            while True:
                time.sleep(1)
                print("Output {} to pin {}".format(curr_value,self.pin_out))
                GPIO.output(self.pin_out,curr_value)
                curr_value ^= GPIO.HIGH
                # if curr_value == GPIO.HIGH:
                #     return True
                # else:
                #     return False
                #time.sleep(1)
        finally:
            GPIO.cleanup()

    def GPIOInput(self,hardwareConnect=False,start_loop_gpio=False):
        try:
            if(hardwareConnect):
                # GPIO.setmode(GPIO.BOARD) 
                # GPIO.setup(7, GPIO.IN)
                # GPIO.setup(13,GPIO.IN)
                # GPIO.setup(15,GPIO.IN)
                # GPIO.setup(29,GPIO.IN)
                while start_loop_gpio:
                    IO1 = GPIO.input(7)
                    IO2 = GPIO.input(13)
                    IO3 = GPIO.input(15)
                    IO4 = GPIO.input(29)
                    if IO1 == GPIO.HIGH:
                        return True
                    elif IO2 == GPIO.HIGH:
                        return True
                    elif IO3 == GPIO.HIGH:
                        return True
                    elif IO4 == GPIO.HIGH:
                        return True
                    else:
                        return False
        # finally:
            # GPIO.cleanup()
        except:
            pass

    def GPIOOutput(self,hardwareConnect=False,start_loop_gpio=False):
        try:
            if(hardwareConnect):
                if start_loop_gpio:
                    IO1 = GPIO.output(31,GPIO.HIGH)
                    IO2 = GPIO.output(33,GPIO.HIGH)
                    IO3 = GPIO.output(35,GPIO.HIGH)
                    IO4 = GPIO.output(37,GPIO.HIGH)
                else:
                    IO1 = GPIO.output(31,GPIO.LOW)
                    IO2 = GPIO.output(33,GPIO.LOW)
                    IO3 = GPIO.output(35,GPIO.LOW)
                    IO4 = GPIO.output(37,GPIO.LOW)

        # finally: 
            # GPIO.cleanup()
        except:
            pass

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

    def testinputFunction(self):
        while True:
            inputdata = (self.testinput(True,True))
            print("Input is {}".format(inputdata))
            if (inputdata):
                return True
                # print("AI state")
            else:
                return False
                # print("input",inputdata)
       

if __name__=="__main__":
    # io = JetsonGPIO()
    # try:
    #     while True:
    #         t1 = time.time()
    #         # res = io.readInput(3)
    #         res = io.readInputDebounce(0)
    #         # io.outputWrite(0,res)
    #         t2 = time.time()
    #         print(f'res = {res} time = {t2-t1}')
    # except:
    #     pass
    
    # io.closeIO()

    io = JetsonGPIO()
    try:
        last_state = False
        while True:
            state = io.readInputDebounce(0)
            if state is not None and state != last_state:
                print(f"State changed: {state}")
                io.outputWrite(0, state)
                last_state = state
            time.sleep(0.1)
    except KeyboardInterrupt:
        print("Interrupted")
    finally:
        io.closeIO()
