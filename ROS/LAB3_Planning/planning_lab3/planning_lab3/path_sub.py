#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from rclpy.qos import QoSProfile
from nav_msgs.msg import Path
import math
# import numpy as np

class my_node (Node):
    def __init__(self):
        super().__init__("sub_node")
        qos_profile = QoSProfile(depth=10)
        self.create_subscription(Path,"/plan",self.timer_call,qos_profile)
        
        self.get_logger().info("subscriber is started")

    def menger_curvature(self, point_1_x, point_1_y, point_2_x, point_2_y, point_3_x, point_3_y):
        triangle_area = 0.5 * abs( (point_1_x*point_2_y) + (point_2_x*point_3_y) + (point_3_x*point_1_y) - (point_2_x*point_1_y) - (point_3_x*point_2_y) - (point_1_x*point_3_y))#Shoelace formula 
            
        curvature = (4*triangle_area) / (math.sqrt(pow(point_1_x - point_2_x,2)+pow(point_1_y - point_2_y,2)) * math.sqrt(pow(point_2_x - point_3_x,2)+pow(point_2_y - point_3_y,2)) * math.sqrt(pow(point_3_x - point_1_x,2)+pow(point_3_y - point_1_y,2)))#Menger curvature 
        return curvature

    def timer_call(self,path_msg):
        path = path_msg.poses
        if len(path)<50:
            point_1 = path[0]
            x1, y1 = point_1.pose.position.x, point_1.pose.position.y 
            point_2 = path[len(path)//2]
            x2, y2 = point_2.pose.position.x, point_2.pose.position.y
            point_3 = path[-1]
            x3, y3 = point_3.pose.position.x, point_3.pose.position.y
        else:
            point_1 = path[0]
            x1, y1 = point_1.pose.position.x, point_1.pose.position.y 
            point_2 = path[10]
            x2, y2 = point_2.pose.position.x, point_2.pose.position.y
            point_3 = path[20]
            x3, y3 = point_3.pose.position.x, point_3.pose.position.y
        
        # self.get_logger().info(str(len(path)))
        curv = self.menger_curvature(x1, y1, x2, y2, x3, y3)
        if curv < 1.0:
            self.get_logger().info("The path is straight")
        else:
            self.get_logger().info(f"The robot is turning with a curvature {curv}")
        # self.get_logger().info(str(curv))
        # self.get_logger().info("Done")

        
        

def main (args=None):
    rclpy.init(args=args)
    node=my_node()
    rclpy.spin(node)

    rclpy.shutdown()


if __name__=="__main__":
    main()


