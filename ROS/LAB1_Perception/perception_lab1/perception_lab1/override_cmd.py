#!/usr/bin/env python3

import rclpy
import numpy as np
import math
from rclpy.node import Node
from rclpy.qos import QoSProfile, qos_profile_sensor_data
from sensor_msgs.msg import LaserScan
from geometry_msgs.msg import Twist

class my_node (Node):
    def __init__(self):
        super().__init__("override_node")

        self.get_logger().info("Override Node is starting now")

        self.qos_profile = QoSProfile(depth=10)
        self.qos_profile_s = qos_profile_sensor_data

        self.current_vel = 0.0
        self.laser_data_45 = []
        self.laser_data_45 = []

        self.create_subscription(LaserScan,"/scan",self.scan_cb, self.qos_profile_s)

        self.create_subscription(Twist,"/key_cmd_vel",self.key_cb,self.qos_profile)
        self.obj_vel = self.create_publisher(Twist,"/cmd_vel",self.qos_profile)
        
        self.create_timer(1/25,self.timer_call)


        
    def scan_cb(self,message):
        laser_data = message.ranges
        self.laser_data_45 = laser_data[:45]
        self.laser_data_315 = laser_data[315:]
        # self.get_logger().info(f"len is {len(laser_data)}")
        # self.get_logger().info(f"len is {len(self.laser_data_45)}")
        # self.get_logger().info(f"len is {len(self.laser_data_315)}")
        # self.get_logger().info(f"min dist_45 is {min(self.laser_data_45)}")
        # self.get_logger().info(f"min dist_315 is {min(self.laser_data_315)}")

        # self.create_subscription(Twist,"/key_cmd_vel",self.key_cb,self.qos_profile)
        # self.obj_vel = self.create_publisher(Twist,"/cmd_vel",self.qos_profile)

        # self.create_timer(1/25,self.timer_call)



    def key_cb(self,vel):
        self.current_vel = vel

    def timer_call(self):
        msg = Twist()
        if self.laser_data_45 == [] or self.laser_data_315 == []:
            self.get_logger().info(f"Wait for lidar to start")
        elif min(self.laser_data_45)<0.5 or min(self.laser_data_315)<0.5:
            if self.current_vel == 0.0:
                pass
            else:
                if self.current_vel.linear.x >= 0.0:
                    msg.linear.x = 0.0
                    msg.linear.y = self.current_vel.linear.y
                    msg.angular.z = self.current_vel.angular.z
                    self.get_logger().info(f"Danger! stop! your velocity is {msg.linear.x}")
                    self.obj_vel.publish(msg)
                else:
                    msg = self.current_vel
                    self.get_logger().info(f"your velocity is {msg.linear.x}")
                    self.obj_vel.publish(msg)
        else:
            if self.current_vel == 0.0:
                pass
                # msg = self.current_vel
                # self.get_logger().info(f"your velocity is {self.current_vel}")
            else:
                msg = self.current_vel
                self.get_logger().info(f"your velocity is {msg.linear.x}")
                self.obj_vel.publish(msg)
          
def main (args=None):
    rclpy.init(args=args)
    node=my_node()
    rclpy.spin(node)
    rclpy.shutdown()

if __name__=="__main__":
    main()


