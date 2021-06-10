#!/usr/bin/env python3

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
        super().__init__("sub_node")
        self.create_subscription(Image,"/intel_realsense_d435_depth/image_raw",self.img_cb, rclpy.qos.qos_profile_sensor_data)
        
        self.get_logger().info("subscriber is started")

        cv2.namedWindow('black', cv2.WINDOW_NORMAL)
        cv2.createTrackbar('maxCorners', 'black', 25, 100, self.nothing)
        cv2.createTrackbar('qualityLevel', 'black', 1, 100, self.nothing)
        cv2.createTrackbar('minDistance', 'black', 10, 20, self.nothing)

    def nothing(self,x):
        pass

    def img_cb(self,message):
        cv2_img = bridge.imgmsg_to_cv2(message, "bgr8")
        gray = cv2.cvtColor(cv2_img,cv2.COLOR_BGR2GRAY)
        black = np.zeros((cv2_img.shape[0],cv2_img.shape[1],3), np.uint8)
        #cv2.imwrite('saved_img.png', cv2_img)

        x = cv2.getTrackbarPos('maxCorners', 'black')
        factor = cv2.getTrackbarPos('qualityLevel', 'black')/100
        if factor==0:
            factor = 0.01
        dist = cv2.getTrackbarPos('minDistance', 'black')

        start_time = time.time()
        corners = cv2.goodFeaturesToTrack(gray,x,factor,dist)
        corners = np.int0(corners)
        end_time = round(time.time() - start_time, 5)
        font = cv2.FONT_HERSHEY_SIMPLEX
        cv2.putText(black, "Execution time is {:0.2f} msec".format(end_time*(10**3)), (25,black.shape[1]-100), font, 0.5, (0, 0, 255), 1, cv2.LINE_AA)

        # cv2.imshow("cv2_img", cv2_img)
        # cv2.imshow("black", black)
        for i in corners:
            x,y = i.ravel()
            cv2.circle(cv2_img,(x,y),3,(255,255,255),-1)
            cv2.circle(black,(x,y),3,255,-1)

        cv2.imshow("cv2_img", cv2_img)
        cv2.imshow("black", black)

        cv2.waitKey(1)

          
def main (args=None):
    rclpy.init(args=args)
    node=my_node()
    rclpy.spin(node)
    rclpy.shutdown()

if __name__=="__main__":
    main()


