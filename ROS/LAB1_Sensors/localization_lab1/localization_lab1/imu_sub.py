#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Imu
from geometry_msgs.msg import Quaternion
from math import sin, cos, pi
import numpy as np
class my_node (Node):
    def __init__(self):
        super().__init__("sub_node")
        self.create_subscription(Imu,"/imu",self.timer_call,10)
        
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

    def timer_call(self,imu_msg):

        _,_,z = self.euler_from_quaternion(imu_msg.orientation)

        if z<=2 or z>=-2:
            self.get_logger().info(f"The robot is nearly heading north .. Heading is: {z} degrees")
        
        if imu_msg.linear_acceleration.x>0.3:
            self.get_logger().warn(f"Warning !! .. linear acceleration x exceeded the limit . Current acceleration is {imu_msg.linear_acceleration.x} m/s^2")

        if imu_msg.angular_velocity.z>0.3:
            self.get_logger().warn(f"Warning !! .. angular velocity z exceeded the limit . Current Angular velocity is {imu_msg.angular_velocity.z} rad/s")


           
      


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


