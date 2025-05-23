import time
from pathlib import Path
from datetime import datetime
import cv2
import torch
import torch.backends.cudnn as cudnn
import numpy as np
from models.experimental import attempt_load
from utils.datasets import LoadImages
from utils.general import (
    check_img_size, non_max_suppression, scale_coords,
    xyxy2xywh, set_logging
)
from utils.plots import plot_one_box
from utils.torch_utils import time_synchronized, TracedModel
import os

class Detector:
    def __init__(self, weights_path, img_size=640, trace=True):
        set_logging()
        self.device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
        self.half = self.device.type != 'cpu'
        self.img_size = check_img_size(img_size)

        # Load model
        self.model = attempt_load(weights_path, map_location=self.device)
        self.stride = int(self.model.stride.max())
        if trace:
            self.model = TracedModel(self.model, self.device, self.img_size)
        if self.half:
            self.model.half()

        self.names = self.model.module.names if hasattr(self.model, 'module') else self.model.names
        self.colors = [[np.random.randint(0, 255) for _ in range(3)] for _ in self.names]

        if self.device.type != 'cpu':
            dummy = torch.zeros(1, 3, self.img_size, self.img_size).to(self.device)
            self.model(dummy.half() if self.half else dummy)

    def detect(self, source_path, save_dir):
        dataset = LoadImages(source_path, img_size=self.img_size, stride=self.stride)

        for path, img, im0s, _ in dataset:
            img_tensor = torch.from_numpy(img).to(self.device)
            img_tensor = img_tensor.half() if self.half else img_tensor.float()
            img_tensor /= 255.0
            if img_tensor.ndimension() == 3:
                img_tensor = img_tensor.unsqueeze(0)

            t1 = time_synchronized()
            with torch.no_grad():
                pred = self.model(img_tensor, augment=False)[0]
            t2 = time_synchronized()

            pred = non_max_suppression(pred, 0.5, 0.45)
            t3 = time_synchronized()

            filename = os.path.basename(source_path)

            result = self.process(pred, im0s, path, save_dir, t2 - t1, t3 - t2, img_tensor.shape[2:], filename)
            if result is not None:
                return result
            else:
                return None

    def process(self, predictions, im0s, path, save_dir, infer_time, nms_time, img_shape,filename):
        Path(save_dir).mkdir(parents=True, exist_ok=True)
        # filename = datetime.now().strftime("%Y-%m-%d-%H-%M-%S-%f")
        save_path = Path(save_dir) / f"{filename}.jpg"

        res = []

        for det in predictions:
            if len(det):
                det[:, :4] = scale_coords(img_shape, det[:, :4], im0s.shape).round()

                for *xyxy, conf, cls in reversed(det):
                    label = f'{self.names[int(cls)]} {conf:.2f}'
                    position = plot_one_box(xyxy, im0s, label=label, color=self.colors[int(cls)], line_thickness=1)
                    res.append(position)

        cv2.imwrite(str(save_path), im0s)
        print(f"Saved: {save_path}")
        print(f"Done. ({infer_time * 1E3:.1f}ms Inference, {nms_time * 1E3:.1f}ms NMS)")
        
        return res if len(res) > 0 else None

if __name__ == '__main__':

    detector = Detector(weights_path=r'/home/vpd/Desktop/BG/yolov7/BG01.pt')
    print('Initialized detector.')
    res = detector.detect(source_path=r'/home/vpd/Desktop/BG/yolov7/4.bmp',
                    save_dir=r'/home/vpd/Desktop/BG/yolov7/DetectionImage')
    print(res)

    # detector = Detector(weights_path=r'D:\fern2022\Backgrinding\dev_test\yolov7\BG01.pt')
    # print('Initialized detector.')
    # res = detector.detect(source_path=r'D:\fern2022\Backgrinding\dev_test\yolov7\4.bmp',
    #                 save_dir=r'D:\fern2022\Backgrinding\dev_test\yolov7\DetectionImage')
    # print(res)