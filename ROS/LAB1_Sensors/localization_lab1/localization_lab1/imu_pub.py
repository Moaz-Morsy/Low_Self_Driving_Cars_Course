#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from rclpy.qos import qos_profile_sensor_data
from sensor_msgs.msg import Imu
from geometry_msgs.msg import Quaternion
from math import sin, cos, pi
import csv
# import numpy as np

class my_node (Node):
    def __init__(self):
        super().__init__("Node_name")
        self.row = 0
        with open('/home/moaz/ROS_WS/src/localization_lab1/localization_lab1/imu_data.csv') as file:
            reader=csv.reader(file)
            self.values=[row for row in reader]
        self.get_logger().info("Node is started")
        self.obj_pub=self.create_publisher(Imu,"zed2_imu",qos_profile_sensor_data)
        self.imu_msg = Imu()
        self.imu_msg.header.frame_id= "zed2_imu_link"
        self.create_timer(1/30,self.timer_call)


    def quaternion_from_euler(self, roll, pitch, yaw):
        qx = sin(roll/2) * cos(pitch/2) * cos(yaw/2) - cos(roll/2) * sin(pitch/2) * sin(yaw/2)
        qy = cos(roll/2) * sin(pitch/2) * cos(yaw/2) + sin(roll/2) * cos(pitch/2) * sin(yaw/2)
        qz = cos(roll/2) * cos(pitch/2) * sin(yaw/2) - sin(roll/2) * sin(pitch/2) * cos(yaw/2)
        qw = cos(roll/2) * cos(pitch/2) * cos(yaw/2) + sin(roll/2) * sin(pitch/2) * sin(yaw/2)
        return Quaternion(x=qx, y=qy, z=qz, w=qw)
    
    def timer_call(self):
        self.imu_msg.header.stamp = self.get_clock().now().to_msg()
        # self.get_logger().info(str(self.imu_msg.header.stamp))
        
        self.imu_msg.orientation.w = 0.0
        self.imu_msg.orientation.x = 0.0
        self.imu_msg.orientation.y = 0.0
        self.imu_msg.orientation.z = self.quaternion_from_euler(0.0, 0.0, float(self.values[self.row][-1])).z
        #self.imu_msg.orientation_covariance = [0.01, 0.0, 0.0, 0.0, 0.01, 0.0, 0.0, 0.0, 0.001]
        # angular velocity
        self.imu_msg.angular_velocity.x = float(self.values[self.row][3])
        self.imu_msg.angular_velocity.y = float(self.values[self.row][4])
        self.imu_msg.angular_velocity.z = float(self.values[self.row][5])
        #self.imu_msg.angular_velocity_covariance=[0.0001, 0.0, 0.0, 0.0, 0.0001, 0.0, 0.0, 0.0, 0.1]
        if self.imu_msg.angular_velocity.z<0.3:
            self.get_logger().info(f"less than 0.3, row {self.row}")
            self.get_logger().info(str(self.imu_msg.orientation.z))
            self.imu_msg.orientation_covariance = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0001]
            self.imu_msg.angular_velocity_covariance=[0.0001, 0.0, 0.0, 0.0, 0.0001, 0.0, 0.0, 0.0, 0.0001]
        else:
            self.get_logger().info(f"larger than 0.3, row {self.row}")
            self.imu_msg.orientation_covariance = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.1]
            self.imu_msg.angular_velocity_covariance=[0.0001, 0.0, 0.0, 0.0, 0.0001, 0.0, 0.0, 0.0, 0.1]

        # linear acceleration
        self.imu_msg.linear_acceleration.x = float(self.values[self.row][0])*9.8
        self.imu_msg.linear_acceleration.y = float(self.values[self.row][1])*9.8
        self.imu_msg.linear_acceleration.z = float(self.values[self.row][2])*9.8
        self.imu_msg.linear_acceleration_covariance=[0.0001, 0.0, 0.0, 0.0, 0.0001, 0.0, 0.0, 0.0, 0.0001]
        self.obj_pub.publish(self.imu_msg)
        # self.row += 1
        if self.row==len(self.values)-1:
            self.row = 0
            self.get_logger().info("Repeat")
        else:
            self.row += 1



def main (args=None):
    rclpy.init(args=args)
    node=my_node()
    rclpy.spin(node)

    rclpy.shutdown()


if __name__=="__main__":
    main()


