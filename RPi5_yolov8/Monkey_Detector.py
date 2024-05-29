import os

import cv2
from yolo_manager import YoloDetectorWrapper
from utils import draw_annotation, sendLineNotify, sendWebNotify
import time
from picamera2 import Picamera2

class Detector():
    def __init__(self):
        # self.detect_frame = True
        self.should_run = True
        self.yolo_detector = YoloDetectorWrapper("/home/anon/Desktop/Mine_Project/RPi5_yolov8/models/nano_dataset_v8.pt")
        self.target_indices = {0}
        self.detection_counter = FrameCounter(self.target_indices, 2)
        self.lockerstatus=False
        # 加入這行
        self.wait_no_warning = False

    def run(self):
        picam2 = Picamera2()
        camera_config = picam2.create_video_configuration(main={"size":(640,640),"format":"RGB888"}, raw={"size": (640, 640)})
        try:   
            picam2.configure(camera_config)
            picam2.start()
        except Exception as e:
            print(f"Failed to start camera: {e}")
            return 
        try:
            while self.should_run:
                try:
                    # 已經在猴子警告時
                    # 等待 20秒 才偵測
                    if self.wait_no_warning:
                        time.sleep(20)

                    frame = picam2.capture_array()
                    frame = cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)
                    if frame is not None:
                    #    if self.detect_frame:
                    	self.process_frame(frame)
                            # self.detect_frame = False
                    else:
                        time.sleep(0.0001)
                except Exception as e:
                        print(f"Failed to process frame: {e}")
        finally:
            picam2.stop()
            print('Detector finished!')

    def process_frame(self, cv_img):
        results = self.yolo_detector.predict(cv_img)
        if self.yolo_detector is None:
            result_image = draw_annotation(cv_img, self.yolo_detector.get_label_names(), results)
            if self.detection_counter.check_detection_results(results):
                if(self.lockerstatus==False):
                    print("Lock\r\n")
                    # sendLineNotify移到外面
                    # sendLineNotify(result_image)
                    self.lockerstatus=True
                else:
                    print("Already Locked\r\n")
                    # 這行不需要 持續執行
                    # self.should_run=False

                # 如果有猴子 wait_no_warning = True
                self.wait_no_warning = True
                sendLineNotify(result_image)
                # 如果有猴子 發送警告到server
                sendWebNotify()

    def stop(self):
        self.should_run = False


class FrameCounter:
    def __init__(self, detection_target_indices, num_frames):
        self.num_frames = num_frames
        self.detection_target_indices = detection_target_indices
        self.counter = 0

    def check_detection_results(self, detection_results):
        target_found = False
        for detection_result in detection_results:
            if len(detection_result.boxes) > 0:
                cls_id = int(detection_result.boxes.cls[0])
                if cls_id in self.detection_target_indices:
                    target_found = True
                    break
        if target_found:
            self.counter += 1
        else:
            self.counter = 0
        return self.counter >= self.num_frames

if __name__ == "__main__":
    video_thread = Detector()
    video_thread.run()
    
