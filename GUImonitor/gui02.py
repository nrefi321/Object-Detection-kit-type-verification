import tkinter as tk
from tkinter import ttk,simpledialog
from PIL import Image,ImageTk
import time
from tkinter.messagebox import showwarning,showerror,showinfo,askyesno
import json
import cv2 
import numpy as np

# from functools import partial

class Guimonitor:
    def __init__(self):
        self.resourcePath = r'D:\fern\project_Fern\Backgrinding_jetson\BackGrinding_check\resourceimage'
        self.root = tk.Tk()
        self.root.title('Status UI')
        # self.root.geometry('1000x700')
        self.root.geometry('1100x700+250+200')
        # self.root.config(bg='#616161')
        # self.root.attributes("-fullscreen", True)

 
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        self.root.resizable(False,False)

        notebook = ttk.Notebook(self.root)
        notebook.grid(row=0,column=0,padx=20,pady=10)
        # notebook.grid_columnconfigure(0, weight=3)
        # notebook.grid_rowconfigure(0, weight=3)

        self.frame1 = ttk.Frame(notebook, width=1000, height=700)
        self.frame2 = ttk.Frame(notebook, width=1000, height=700)

        notebook.add(self.frame1, text='Monitor')
        notebook.add(self.frame2, text='Config')
        self.Monitor()
        self.Config()

    def Monitor(self):
        # self.lightFrame = tk.Frame(self.root)
        self.lightFrame = tk.Frame(self.frame1)
        self.lightFrame.grid(row=0,column=0, sticky='news',pady=10)
        self.lightFrame.grid_columnconfigure(0, weight=3)
        self.lightFrame.grid_rowconfigure(0, weight=3)

        # self.imgFrame = tk.Frame(self.root)
        self.imgFrame = tk.Frame(self.frame1)
        self.imgFrame.grid(row=1,column=0, sticky='news')
        self.imgFrame.grid_columnconfigure(0, weight=3)
        self.imgFrame.grid_rowconfigure(0, weight=3)

        light = tk.PhotoImage(file=f'{self.resourcePath}\gray.png')
        light.img = light

        self.imgpath = f'{self.resourcePath}\imgfree.jpg'
        img=Image.open(f'{self.resourcePath}\imgfree.jpg')
        resized_image= img.resize((600,360))
        new_image= ImageTk.PhotoImage(resized_image)
        new_image.img = new_image

        # canvas = tk.Canvas(self.root)
        # canvas.create_rectangle(20, 20, 120, 80, outline="#fb0")

        self.light = tk.Label(self.lightFrame, image=light)
        self.light.grid(row=0, column=0, sticky='news')
        self.newimg = tk.Label(self.imgFrame,image=new_image)
        self.newimg.grid(row=1,column=0,sticky='news',padx=(20,20), pady=(20,20))

        self.lbState = tk.Label(master=self.frame1, text="State")
        self.lbState.grid(row=0, column=1, padx=(60,60), pady=(120,0)) 
        self.lbState.config(font=("Tahoma", 18),width=25)

        self.lbText = tk.Label(master=self.frame1, text="Test")
        self.lbText.grid(row=0, column=1, padx=(60,60), pady=(185,0)) 
        self.lbText.config(font=("Tahoma", 18),width=25 , background='#c5cae9')

        self.lbStatus = tk.Label(master=self.frame1, text="Status")
        self.lbStatus.grid(row=0, column=1, padx=(60,60), pady=(0,50))
        self.lbStatus.config(font=("Tahoma", 20), width=10)

        self.lbResult = tk.Label(master=self.frame1, text="Start")
        self.lbResult.grid(row=0, column=1, padx=(60,60), pady=(60,30))
        self.lbResult.config(font=("Tahoma", 20), width=10 ,bg='lightgray')

        self.btStop = tk.Button(master=self.frame1, text="STOP",command=self.stop)
        self.btStop.grid(row=1, column=1, padx=(60,60), pady=(0,80))
        self.btStop.config(font=("Tahoma", 16), width=10)
        self.btStop.bind('<ButtonRelease-1>')

        self.btReset = tk.Button(master=self.frame1, text="RESET",command=self.reset)
        
        self.btReset.grid(row=1, column=1, padx=(60,60), pady=(50,10))
        self.btReset.config(font=("Tahoma", 16), width=10)
        self.btReset.config(command=self.onReset)
        self.btReset.bind('<ButtonRelease-1>')
        self.clicked = False

        self.reset_callback = None    
        self.imgpath = None
        # self.stateStatus('s1')
        # self.frame1.config()
        # style = ttk.Style()
        # style.configure("Custom.TFrame", background="#616161")  # Define a new style for blue background
        # self.frame1.configure(style="Custom.TFrame") 


    def stateStatus(self,state):
        # if state is not None:
        # print(f'state status {state} {type(state)}')
        # state = state.strip()
        # print(state == 's1')
        if state == 's1':
            self.lbState["text"] = "S1 : Checking the door"
            # self.lbState = tk.Label(master=self.frame1, text="State S1 : Checking the door")
            # self.lbState.config(font=("Tahoma", 18),width=25)
        elif state == 's2':
            self.lbState["text"] = "S2 : Waiting for cassette setup"
            # self.lbState.config(font=("Tahoma", 18),width=25)
        elif state == 's3':
            self.lbState["text"] = "S3 : Waiting for AI and analysis"
        elif state == 's4':
            self.lbState["text"] = "S4 : Wrong setup Warning Alarm"
        elif state == 's5':
            self.lbState["text"] = "S5 : Clear stste"
        else:
            self.lbState["text"] = "State xx"
        self.lbState.config(font=("Tahoma", 14),width=40)
        
    def onReset(self):
        if self.reset_callback is not None:
            self.reset_callback()
    
    def set_reset_callback(self, callback):
        self.reset_callback = callback

    def start(self):
        self.root.mainloop()

    def stop(self):
        self.root.destroy()
    
    def clickReset(self):
        self.clicked = True
    
    def reset(self):
        self.lbText["text"] = "Resetting..waiting for data.."
        self.lbText.config(font=("Tahoma", 18), width=25,background='#c5cae9')
        self.lbResult["text"] = "Reset"
        self.lbResult.config(font=("Tahoma", 20), width=10,bg='lightgray')

        light = tk.PhotoImage(file=f'{self.resourcePath}\gray.png')
        light.img = light
        self.light['image'] = light

        img=Image.open(f'{self.resourcePath}\image.jpg')
        resized_image= img.resize((600,360))
        new_image= ImageTk.PhotoImage(resized_image)
        new_image.img = new_image 
        self.newimg['image'] = new_image
    
    def onStop(self):
        self.stop()
        time.sleep(2)
        if self.stop_callback is not None:
            self.stop_callback()
    
    def set_stop_callback(self, callback):
        self.stop_callback = callback

    def guiImagePath(self,imgpath):
        if imgpath is not None:
            self.imgpath = imgpath
        else:
            filename = r"D:\fern\project_Fern\Backgrinding_jetson\BackGrinding_check\resourceimage\imgfree.jpg"
            img = cv2.imread(filename)
            image = Image.fromarray(np.uint8(img))
            self.imgpath = image
        # print(f'Immage GUI {self.imgpath}')
        # print('get img gui')
        
    def check_data(self,res):
        # print(res , state)
        if res:
            light = tk.PhotoImage(file=f'{self.resourcePath}\green.png')
            light.img = light
            self.light['image'] = light

            # img=Image.open(r"D:\fern\project_Fern\Backgrinding_jetson\BackGrinding_check\resourceimage\t1.jpg")
            img=self.imgpath
            resized_image= img.resize((600,360))
            new_image= ImageTk.PhotoImage(resized_image)
            new_image.img = new_image 
            self.newimg['image'] = new_image

            self.lbResult["text"] = "Running"
            self.lbResult.config(font=("Tahoma", 20), width=10,bg='lightgreen')
        elif res == False:
            light = tk.PhotoImage(file=f'{self.resourcePath}\yellow.png')
            light.img = light
            self.light['image'] = light

            # img=Image.open(r"D:\fern\project_Fern\Backgrinding_jetson\BackGrinding_check\resourceimage\t2.jpg")
            # img=Image.open(f"{self.imgpath}")
            img=self.imgpath
            resized_image= img.resize((600,360))
            new_image= ImageTk.PhotoImage(resized_image)
            new_image.img = new_image 
            self.newimg['image'] = new_image

            self.lbResult["text"] = "Warning"
            self.lbResult.config(font=("Tahoma", 20), width=10,bg='yellow')        
        else:
            light = tk.PhotoImage(file=f'{self.resourcePath}\gray.png')
            light.img = light
            self.light['image'] = light

            # img=Image.open(r"D:\fern\project_Fern\Backgrinding_jetson\BackGrinding_check\resourceimage\t2.jpg")
            # img=Image.open(f"{self.imgpath}")
            img=self.imgpath
            # print(f'img type >>>>>>>>>>>>> {type(img)}')
            # img = self.imgpath
            resized_image= img.resize((600,360))
            new_image= ImageTk.PhotoImage(resized_image)
            new_image.img = new_image 
            self.newimg['image'] = new_image

            self.lbResult["text"] = "None"
            self.lbResult.config(font=("Tahoma", 20), width=10,bg='gray')


        # self.lbState = tk.Label(master=self.frame1, text=f"State {state}")
        # self.lbState.config(font=("Tahoma", 18),width=25)

        self.lbText["text"] = "Data received: {}".format(res)
        self.lbText.config(font=("Tahoma", 18), width=25 ,background='#c5cae9')
        # self.stateStatus(state)


####################################################################################################

    def Config(self):
        self.lbConfig = tk.Label(master=self.frame2, text="CONFIG")
        self.lbConfig.grid(row=0, column=0, sticky='nw', padx=(240,60), pady=57) 
        self.lbConfig.config(font=("Tahoma", 18),width=25)
        self.btEdit = tk.Button(master=self.frame2, text="Edit")
        self.btEdit.grid(row=0, column=0, sticky='nw', padx=(480,40), pady=57)
        self.btEdit.config(font=("Tahoma", 12), width=8,command=self.show_password_popup)
        # self.btConfig.config(command=self.onReset)
        self.btEdit.bind('<ButtonRelease-1>')
        self.create_widgets()
    
    def show_password_popup(self):
        try:
            password = simpledialog.askstring("Password", "Enter password:", show='*',parent=self.root)
            if password is None:
                return
            if password == 'password':
                # self.controller.show_frame(Guiconfig)
                self.enable_entry()
        
            
            else:
                # showwarning(title='Warning', message='Wrong password.')
                self.disable_entry()
                showerror(title='Error', message='Wrong password.')
        except TypeError:
            return

    def create_widgets(self):

        self.useAI_var = tk.BooleanVar()
        self.hardwareConnect_var = tk.BooleanVar()
        self.inputChannel_var = tk.IntVar()
        self.outputChannel_var = tk.IntVar()
        self.debouncetime_var = tk.DoubleVar()
        self.combo_var = tk.StringVar()
        self.width_var = tk.IntVar()
        self.height_var = tk.IntVar()
        self.createLabelFrame()
        self.UseAI()
        self.HWconnect()
        self.inputChannel()
        self.outputChannel()
        self.debounceTime()
        self.combobox()
        # # self.HWentry()
        self.disable_entry()
    
    def createLabelFrame(self):
        # self.frame = tk.Frame(self.frame2)
        # self.frame.grid(row=0,column=0, sticky='news')
        # self.frame.grid_columnconfigure(0, weight=3)
        # self.frame.grid_rowconfigure(0, weight=3)
        # create LabelFrames
        self.lf = tk.LabelFrame(self.frame2, text='Config')
        self.lf.grid(column=0,row=0, sticky='news', padx=(100,100), pady=(100,50))
        self.lf.config(font=('calibre',14,'normal'))

        self.lf2 = tk.LabelFrame(self.lf, text='test')
        self.lf2.grid(column=1,row=0,columnspan=2, rowspan=3, sticky='news', padx=(10,10), pady=10)
        self.lf2.config(font=('calibre',12,'normal'))

        self.lf3 = tk.LabelFrame(self.lf2, text='Camera AOI')
        self.lf3.grid(column=0, row=0, sticky='news', padx=20, pady=(200,20))
        self.lf3.config(font=('calibre',12,'normal'))

        self.btDone = tk.Button(master=self.lf, text="Done")
        self.btDone.grid(row=3, column=0,columnspan=2,sticky='nw', padx=(350,10), pady=(40,5))
        self.btDone.config(font=("Tahoma", 12), width=10,command=self.doneEdit)
        # self.btConfig.config(command=self.onReset)
        self.btDone.bind('<ButtonRelease-1>')

    def UseAI(self):
        # useAI radiobuttons
        self.useAI_frame = tk.LabelFrame(self.lf, text='Use AI')
        self.useAI_frame.grid(column=0, row=0, sticky='news', padx=40, pady=30 ,ipadx=10, ipady=0)
        self.useAI_frame.config(font=('calibre',12,'normal'))
        self.rbUse_true = tk.Radiobutton(self.useAI_frame, text='True', variable=self.useAI_var, value=True)
        self.rbUse_true.grid(column=0, row=0, sticky='nw', padx=60, pady=10)
        self.rbUse_true.config(font=('calibre',11,'normal'))
        self.rbUse_false = tk.Radiobutton(self.useAI_frame, text='False', variable=self.useAI_var, value=False)
        self.rbUse_false.grid(column=0, row=0, sticky='nw', padx=60, pady=40)
        self.rbUse_false.config(font=('calibre',11,'normal'))
    
    def HWconnect(self):
        # hardwareConnect radiobuttons
        self.hw_frame = tk.LabelFrame(self.lf, text='Hardware Connect')
        self.hw_frame.grid(column=0, row=1, sticky='news', padx=40, pady=30 ,ipadx=10, ipady=0)
        self.hw_frame.config(font=('calibre',12,'normal'))
        self.rbHW_true = tk.Radiobutton(self.hw_frame, text='True', variable=self.hardwareConnect_var, value=True)
        self.rbHW_true.grid(column=0, row=0, sticky='nw', padx=60, pady=10)
        self.rbHW_true.config(font=('calibre',11,'normal'))
        self.rbHW_false = tk.Radiobutton(self.hw_frame, text='False', variable=self.hardwareConnect_var, value=False)
        self.rbHW_false.grid(column=0, row=0, sticky='nw', padx=60, pady=40)
        self.rbHW_false.config(font=('calibre',11,'normal'))

    def inputChannel(self):
        # inputChannel spinbox
        self.input_label = tk.Label(self.lf2, text='Input Channel :')
        self.input_label.grid(column=0, row=0, sticky='nw', padx=70, pady=40)
        self.input_label.config(font=('calibre',11,'normal'))
        self.input_spinbox = tk.Spinbox(self.lf2, from_=0, to=3, textvariable=self.inputChannel_var)
        self.input_spinbox.grid(column=0, row=0, sticky='nw', padx=(200,40), pady=40)
        self.input_spinbox.config(font=('calibre',11,'normal'))

    def outputChannel(self):
        # outputChannel spinbox
        self.output_label = tk.Label(self.lf2, text='Output Channel :')
        self.output_label.grid(column=0, row=0, sticky='nw', padx=70, pady=90)
        self.output_label.config(font=('calibre',11,'normal'))
        self.output_spinbox = tk.Spinbox(self.lf2, from_=0, to=3, textvariable=self.outputChannel_var)
        self.output_spinbox.grid(column=0, row=0, sticky='nw', padx=(200,40), pady=90)
        self.output_spinbox.config(font=('calibre',11,'normal'))

    def debounceTime(self):
        # debouncetime spinbox
        self.debounce_label = tk.Label(self.lf2, text='Debounce Time :')
        self.debounce_label.grid(column=0, row=0, sticky='nw', padx=70, pady=140)
        self.debounce_label.config(font=('calibre',11,'normal'))
        self.debounce_spinbox = tk.Spinbox(self.lf2, from_=0, to=10, increment=0.1, textvariable=self.debouncetime_var)
        self.debounce_spinbox.grid(column=0, row=0, sticky='nw', padx=(200,40), pady=140)
        self.debounce_spinbox.config(font=('calibre',11,'normal'))

    def combobox(self):
        self.wh_label = tk.Label(self.lf3, text='Width x height :')
        self.wh_label.grid(column=0, row=0, sticky='nw', padx=(40,50), pady=(50,50))
        self.wh_label.config(font=('calibre',11,'normal'))

        windowSize = ('640 x 480','800 x 480','1280 x 720','1280 x 960','1600 x 1200','1920 x 1080','2048 x 1536','2592 x 1944')
        # var = tk.StringVar()
        self.combo_size = ttk.Combobox(self.lf3, textvariable=self.combo_var)
        self.combo_size['values'] = windowSize
        self.combo_size['state'] = 'readonly'
        self.combo_size.grid(column=0, row=0, sticky='news', padx=(150,30), pady=(50,50))
        self.combo_size.config(font=('calibre',11,'normal'))

    def HWentry(self):

        # cameraAOI width entry
        self.width_label = tk.Label(self.lf3, text='Width :')
        self.width_label.grid(column=0, row=0, sticky='nw', padx=(60,40), pady=(40,60))
        self.width_label.config(font=('calibre',11,'normal'))
        self.width_entry = tk.Entry(self.lf3, textvariable=self.width_var)
        self.width_entry.grid(column=0, row=0, sticky='nw', padx=(150,30), pady=(40,60))
        self.width_entry.config(font=('calibre',11,'normal'))

        # cameraAOI height entry
        self.height_label = tk.Label(self.lf3, text='Height :')
        self.height_label.grid(column=0, row=0, sticky='nw', padx=(60,40), pady=(80,20))
        self.height_label.config(font=('calibre',11,'normal'))
        self.height_entry= tk.Entry(self.lf3, textvariable=self.height_var,validate='key')
        self.height_entry.grid(column=0, row=0, sticky='nw', padx=(150,30), pady=(80,20))
        self.height_entry.config(font=('calibre',11,'normal'))
        
    def confirm(self):
        answer = askyesno(title='Confirmation',
                          message='Are you sure that you want edit ?')
        if answer:
            print('access to edit')
            self.enable_entry()
        else:
            self.disable_entry()
    
    def disable_entry(self):
        # self.width_entry.config(state= "disabled")
        # self.height_entry.config(state= "disabled")
        self.debounce_spinbox.config(state= "disabled")
        self.output_spinbox.config(state= "disabled")
        self.input_spinbox.config(state= "disabled")
        self.rbUse_true.config(state= "disabled")
        self.rbUse_false.config(state= "disabled")
        self.rbHW_true.config(state= "disabled")
        self.rbHW_false.config(state= "disabled")
        self.combo_size.config(state="disabled")
    
    def enable_entry(self):
        # self.width_entry.config(state="normal")
        # self.height_entry.config(state="normal")
        self.debounce_spinbox.config(state="normal")
        self.output_spinbox.config(state="normal")
        self.input_spinbox.config(state="normal")
        self.rbUse_true.config(state="normal")
        self.rbUse_false.config(state="normal")
        self.rbHW_true.config(state="normal")
        self.rbHW_false.config(state="normal")
        self.combo_size.config(state="normal")

    def doneEdit(self):
        answer = askyesno(title='Confirmation',
                          message='Are you sure that you want to change ?')
        if answer:
            print('Done')
            self.disable_entry()
            self.ondoneEdit()
            self.recipe()
            # save config

    def ondoneEdit(self):
        if self.doneEdit_callback is not None:
            self.doneEdit_callback()
    
    def set_doneEdit_callback(self, callback):
        self.doneEdit_callback = callback
    
    def writeToJSONFile(self,config_dir,param):
        json_data = json.dumps(param, indent=2)
        f = open(config_dir, 'w')
        f.write(json_data)
        f.close()

    def recipe(self):
        useAI = self.useAI_var.get()
        hardwareConnect = self.hardwareConnect_var.get()
        inputChannel = self.inputChannel_var.get()
        outputChannel = self.outputChannel_var.get()
        debouncetime = self.debouncetime_var.get()
        sizeselect = self.combo_var.get()
        # width = self.width_var.get()
        # height = self.height_var.get()

        # print(size)
        size = sizeselect.split(" ")
        w = int(size[0])
        h = int(size[2])
        print("Size:",sizeselect)
        param = {"useAI": useAI, "hardwareConnect": hardwareConnect, "inputChannel": inputChannel, "outputChannel": outputChannel, "debouncetime": debouncetime, "cameraAOI": {"width": w, "height": h}}
        print(param)
        path = r'D:\fern\project_Fern\Backgrinding_jetson\BG-ui\configtest.json'
        self.writeToJSONFile(path,param)



if __name__ == '__main__':
    try:
        proc = Guimonitor()
        
        proc.start()
    except Exception as e:
        print(e)
