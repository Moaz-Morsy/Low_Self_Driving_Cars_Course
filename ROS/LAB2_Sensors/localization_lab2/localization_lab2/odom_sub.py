#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from rclpy.qos import QoSProfile
from nav_msgs.msg import Odometry
from geometry_msgs.msg import Quaternion
from math import sin, cos, pi
import numpy as np
import csv

class my_node (Node):
    def __init__(self):
        super().__init__("sub_node")
        qos_profile = QoSProfile(depth=10)
        with open('/home/moaz/ROS_WS/src/localization_lab2/localization_lab2/pose.csv') as file:
            reader=csv.reader(file)
            self.values=[row for row in reader]
        self.x_val = 0
        self.y_val = 0
        self.yaw_val = 0
        self.row = 1
        self.cond = False
        self.create_subscription(Odometry,"/odom",self.timer_call,qos_profile)
        
        self.get_logger().info("subscriber is started")

    def euler_from_quaternion(self, quaternion):
        x = quaternion.x
        y = quaternion.y
        z = quaternion.z
        w = quaternion.w

        sinr_cosp = 2 * (w * x + y * z)
        cosr_cosp = 1 - 2 * (x * x + y * y)
        roll = np.arctan2(sinr_cosp, cosr_cosp)

        sinp = 2 * (w * y - z * x)
        pitch = np.arcsin(sinp)

        siny_cosp = 2 * (w * z + x * y)
        cosy_cosp = 1 - 2 * (y * y + z * z)
        yaw = np.arctan2(siny_cosp, cosy_cosp)

        return roll, pitch, yaw

    def timer_call(self,odom_msg):
        if self.row<len(self.values):
            self.x_val = float(self.values[self.row][0])
            self.y_val = float(self.values[self.row][1])
            self.yaw_val = float(self.values[self.row][2])

        _,_,yaw = self.euler_from_quaternion(odom_msg.pose.pose.orientation)
        yaw = yaw*(180/pi)
        x = odom_msg.pose.pose.position.x
        y = odom_msg.pose.pose.position.y

        if self.row>len(self.values)-1:
            self.get_logger().error(f"I execute all position and last one is x: {self.x_val}, y: {self.y_val}, theta: {self.yaw_val}")
        elif abs(self.yaw_val-yaw)<=7.5 and abs(self.x_val-x)<=1.5 and abs(self.y_val-y)<=1.5:
            self.get_logger().warn(f"The robot is nearly the required position in csv at row: {self.row}")
            self.row += 1
            self.cond = True
        else:
            self.get_logger().info(f"The robot is not there yet, it's current postion x: {x}, y: {y}, theta: {yaw}")
            if self.cond:
                self.get_logger().warn(f"The robot's previous position in csv at row: {self.row-1}, go to next position in csv at row: {self.row}")
        


def quaternion_from_euler(self, roll, pitch, yaw):
        qx = sin(roll/2) * cos(pitch/2) * cos(yaw/2) - cos(roll/2) * sin(pitch/2) * sin(yaw/2)
        qy = cos(roll/2) * sin(pitch/2) * cos(yaw/2) + sin(roll/2) * cos(pitch/2) * sin(yaw/2)
        qz = cos(roll/2) * cos(pitch/2) * sin(yaw/2) - sin(roll/2) * sin(pitch/2) * cos(yaw/2)
        qw = cos(roll/2) * cos(pitch/2) * cos(yaw/2) + sin(roll/2) * sin(pitch/2) * sin(yaw/2)
        return Quaternion(x=qx, y=qy, z=qz, w=qw)



def main (args=None):
    rclpy.init(args=args)
    node=my_node()
    rclpy.spin(node)

    rclpy.shutdown()


if __name__=="__main__":
    main()


