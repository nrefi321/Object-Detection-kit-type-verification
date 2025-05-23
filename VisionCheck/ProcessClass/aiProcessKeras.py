import numpy as np
import glob
import cv2 as cv
import tensorflow.keras
from tensorflow.keras.models import load_model
# from keras.models import load_model
from PIL import Image, ImageOps

class ProcAIKeras:
    def __init__(self):
        self.pathModel = r"/home/vpd/Desktop/BG_test/BackGrinding_keras/keras_model.h5" 
        self.model = load_model(self.pathModel)
        self.data = np.ndarray(shape=(1, 224, 224, 3), dtype=np.float32)
        # self.frame = frame
    
    def aiKerasProc(self,frame):
        image_array = cv.resize(frame,(224,224),interpolation=cv.INTER_NEAREST)
        normalized_image_array = (image_array.astype(np.float32) / 127.0) - 1
        self.data[0] = normalized_image_array

        prediction = self.model.predict(self.data)[0]

        if(prediction[0] > prediction[1]):
            print("Good {}".format(prediction[0]))
            return True
            # cv.putText( img_show, "Good", (10, 20),
            # cv.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
        else:
            print('Reject {}'.format(prediction[0]))
            return False
            # cv.putText( img_show, "Reject", (10, 20),
            # cv.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)

if __name__ == "__main__":
    
    img = cv.imread(r"/home/vpd/Desktop/BG_test/BackGrinding_keras/Image BG TEST/GOOD/GD5.bmp")
    # img = cv.imread(r"D:\fern\project_Fern\BackGrinding\BackGrinding_keras\Image BG TEST\Reject\RJ4.bmp")
    # path = r"D:\fern\project_Fern\BackGrinding\BackGrinding_keras\keras_model.h5"
    proc = ProcAIKeras()
    res = proc.aiKerasProc(img)
    print(res)
    

    