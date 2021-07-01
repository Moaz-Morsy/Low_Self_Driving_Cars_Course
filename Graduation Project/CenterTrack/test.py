#!/usr/bin/env python3

import sys
import cv2
# import glob

CENTERTRACK_PATH = "/home/moaz/Desktop/test_tracking/CenterTrack/src/lib"
sys.path.append(CENTERTRACK_PATH)

from detector import Detector
from opts import opts

MODEL_PATH = "/home/moaz/Desktop/test_tracking/CenterTrack/models/nuScenes_3Dtracking.pth"
# MODEL_PATH = "/home/moaz/Desktop/test_tracking/CenterTrack/models/coco_pose_tracking.pth"
TASK = "tracking,ddd" # or 'tracking,multi_pose' for pose tracking and 'tracking,ddd' for monocular 3d tracking
# TASK = "tracking,multi_pose"
DATASET = "nuscenes"
# DATASET = "coco"
THRESHOLD = 0.1
opt = opts().init("{} --load_model {} --dataset {} --pre_hm --track_thresh {} --debug 2 --test_focal_length 633".format(TASK, MODEL_PATH,DATASET,THRESHOLD).split(' '))
# print(opt)
detector = Detector(opt)
detector.pause = False

# cap = cv2.VideoCapture('/home/moaz/Desktop/test_tracking/CenterTrack/videos/nuscenes_mini.mp4')
cap = cv2.VideoCapture('/home/moaz/Desktop/test_tracking/CenterTrack/videos/nuscenes_mini.mp4')
# cap = cv2.VideoCapture(0) # For reading from camera 

# cnt = 0
while (cap.isOpened()):
    ret, frame = cap.read()
    if (ret):
        # cv2.imwrite('vid/Frame_{}.jpg'.format(cnt), frame)
        # cnt += 1
        cv2.imshow('Frame', frame)
        out = detector.run(frame)['results']
        # print(out)
        k = cv2.waitKey(1)
        if k == ord('q'):
            break
            
    else:
        break
print(out[0].keys())
for dict in out:
    print(dict['tracking_id'], dict['dep'])
cv2.destroyAllWindows()

# img_array = []
# for filename in glob.glob('vid/*.jpg'):
#     img = cv2.imread(filename)
#     height, width, layers = img.shape
#     size = (width,height)
#     img_array.append(img)

# for img in img_array:
#   ret = detector.run(img)['results']
#   continue