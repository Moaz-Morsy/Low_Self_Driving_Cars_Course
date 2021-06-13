#!/usr/bin/env python3

from numpy.lib import average
import rclpy
import numpy as np
import math
from rclpy.node import Node
from sensor_msgs.msg import Image
from cv_bridge import CvBridge, CvBridgeError
# OpenCV2 for saving an image
import cv2
import time

# Instantiate CvBridge
bridge = CvBridge()

class my_node (Node):
    def __init__(self):
        super().__init__("orb_sub_node")
        self.create_subscription(Image,"/intel_realsense_d435_depth/image_raw",self.img_cb, rclpy.qos.qos_profile_sensor_data)
        
        self.get_logger().info("subscriber is started")
        self.flag = False
        self.prev_frame = 0
        # self.diff_x = []
        # self.diff_y = []

        cv2.namedWindow("Output")

    def nothing(self,x):
        pass

    def img_cb(self,message):

        # read images
        current_frame = bridge.imgmsg_to_cv2(message, "bgr8")
        # prev_frame = current_frame
        
        # sift
        if self.flag == True:
            gray_1 = cv2.cvtColor(self.prev_frame, cv2.COLOR_BGR2GRAY)
            gray_2 = cv2.cvtColor(current_frame, cv2.COLOR_BGR2GRAY)
            orb = cv2.ORB_create()
            t0 = time.time()
            keypoints_1, descriptors_1 = orb.detectAndCompute(gray_1, None)
            keypoints_2, descriptors_2 = orb.detectAndCompute(gray_2, None)

            # feature matching
            if descriptors_1 is not None and  descriptors_2 is not None:
                bf = cv2.BFMatcher(cv2.NORM_L1, crossCheck=True)
                matches = bf.match(descriptors_1, descriptors_2)
                matches = sorted(matches, key = lambda x:x.distance)
                end_time = time.time() - t0

                diff_x = []
                diff_y = []

                if matches is not None:
                    # for match in matches:
                    #     # try:
                    #     # print(match)
                    #     print(match.queryIdx,match.trainIdx)
                    #     print(len(keypoints_1),len(keypoints_2))
                        #     # list_kp1 = [kp1[mat.queryIdx].pt for mat in matches] 
                    #     # list_kp2 = [kp2[mat.trainIdx].pt for mat in matches]
                    #     diff_x.append(keypoints_2[match.queryIdx].pt[0]-keypoints_1[match.trainIdx].pt[0])
                    #     diff_y.append(keypoints_2[match.queryIdx].pt[1]-keypoints_1[match.trainIdx].pt[1])
                    #     # except Exception as e:
                    #         # continue

                    list_kp2 = [keypoints_1[mat.queryIdx].pt for mat in matches] 
                    list_kp1 = [keypoints_2[mat.trainIdx].pt for mat in matches]

                    # print(list_kp1)
                    # print(list_kp2)

                    # print(list_kp2[i][0]-list_kp1[i][0] for i in range(len(list_kp1)))

                    # diff_x.append(list_kp2[i][0]-list_kp1[i][0] for i in range(len(list_kp1)))
                    # diff_y.append(list_kp2[i][1]-list_kp1[i][1] for i in range(len(list_kp1)))

                    # print(diff_x)
                    # print(diff_y)

                    for i in range(len(list_kp1)):
                        diff_x.append(list_kp2[i][0]-list_kp1[i][0])
                        diff_y.append(list_kp2[i][1]-list_kp1[i][1])

                    avg_x = sum(diff_x)/len(diff_x)
                    avg_y = sum(diff_y)/len(diff_y)
                    # show results
                    output = cv2.drawMatches(self.prev_frame, keypoints_1, current_frame, keypoints_2, matches, current_frame, flags=2)
                    # print(current_frame.shape[0],current_frame.shape[1])
                    # print(output.shape[0],output.shape[1])
                    pt1 = (output.shape[1]//2,output.shape[0]//2)
                    pt2 =  (output.shape[1]//2+int(avg_x),output.shape[0]//2+int(avg_y)) #(int(avg_x),int(avg_y))
                    # font = cv2.FONT_HERSHEY_SIMPLEX
                    cv2.arrowedLine(output, pt1, pt2,(0,255,0),5)
                    # print(output.shape[0],output.shape[1])
                    # print(output.shape[0]//2,output.shape[1]//2)
                    # print(avg_x,avg_y)
                    # cv2.putText(output, "Execution time is {:0.2f} msec".format(end_time*(10**3)), (output.shape[0]-20,output.shape[1]-1//2), font, 0.5, (0, 0, 255), 1, cv2.LINE_AA)
                    cv2.imshow("Output", output)
                    cv2.waitKey(1)
                    self.get_logger().info("Execution time is {:0.2f} msec".format(end_time*(10**3)))
                    self.flag = False
        else:
            self.prev_frame = current_frame
            self.flag = True


          
def main (args=None):
    rclpy.init(args=args)
    node=my_node()
    rclpy.spin(node)
    rclpy.shutdown()

if __name__=="__main__":
    main()


