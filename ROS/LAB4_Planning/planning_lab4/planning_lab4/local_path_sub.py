#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from rclpy.qos import QoSProfile
from nav_msgs.msg import Path
import math
import numpy as np

class my_node (Node):
    def __init__(self):
        super().__init__("sub_node")
        qos_profile = QoSProfile(depth=10)
        self.create_subscription(Path,"/local_plan",self.timer_call,qos_profile)
        
        self.get_logger().info("subscriber is started")

    def euler_from_quaternion(self, quaternion):
        """
        Converts quaternion (w in last place) to euler roll, pitch, yaw
        quaternion = [x, y, z, w]
        Bellow should be replaced when porting for ROS 2 Python tf_conversions is done.
        """
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

    def menger_curvature(self, point_1_x, point_1_y, point_2_x, point_2_y, point_3_x, point_3_y):
        triangle_area = 0.5 * abs( (point_1_x*point_2_y) + (point_2_x*point_3_y) + (point_3_x*point_1_y) - (point_2_x*point_1_y) - (point_3_x*point_2_y) - (point_1_x*point_3_y))#Shoelace formula 
            
        curvature = (4*triangle_area) / (math.sqrt(pow(point_1_x - point_2_x,2)+pow(point_1_y - point_2_y,2)) * math.sqrt(pow(point_2_x - point_3_x,2)+pow(point_2_y - point_3_y,2)) * math.sqrt(pow(point_3_x - point_1_x,2)+pow(point_3_y - point_1_y,2)))#Menger curvature 
        return curvature

    def timer_call(self,path_msg):
        path = path_msg.poses
        if path != []:
            if len(path)<13:
                point_1 = path[0]
                x1, y1 = point_1.pose.position.x, point_1.pose.position.y
                _,_,yaw1 = self.euler_from_quaternion(point_1.pose.orientation)
                yaw1 = yaw1*(180/math.pi) 
                point_2 = path[len(path)//2]
                x2, y2 = point_2.pose.position.x, point_2.pose.position.y
                _,_,yaw2 = self.euler_from_quaternion(point_2.pose.orientation)
                yaw2 = yaw2*(180/math.pi)
                point_3 = path[-1]
                x3, y3 = point_3.pose.position.x, point_3.pose.position.y
                _,_,yaw3 = self.euler_from_quaternion(point_3.pose.orientation)
                yaw3 = yaw3*(180/math.pi)
            else:
                point_1 = path[0]
                x1, y1 = point_1.pose.position.x, point_1.pose.position.y
                _,_,yaw1 = self.euler_from_quaternion(point_1.pose.orientation)
                yaw1 = yaw1*(180/math.pi) 
                point_2 = path[5]
                x2, y2 = point_2.pose.position.x, point_2.pose.position.y
                _,_,yaw2 = self.euler_from_quaternion(point_2.pose.orientation)
                yaw2 = yaw2*(180/math.pi)
                point_3 = path[10]
                x3, y3 = point_3.pose.position.x, point_3.pose.position.y
                _,_,yaw3 = self.euler_from_quaternion(point_3.pose.orientation)
                yaw3 = yaw3*(180/math.pi)
            
        
            # self.get_logger().info("path length is: "+str(len(path)))
            try:
                curv = self.menger_curvature(x1, y1, x2, y2, x3, y3)
                if curv < 1.0:
                    self.get_logger().info("The path is straight")
                else:
                    if yaw1<yaw2 and yaw2<yaw3:
                        self.get_logger().info(f"The robot is turning left with a curvature {curv}")
                        self.get_logger().info(f"yaw1 is: {yaw1}, yaw2 is: {yaw2}, yaw3 is: {yaw3}")
                        self.get_logger().info("Done")
                    elif yaw1>yaw2 and yaw2>yaw3:
                        self.get_logger().info(f"The robot is turning right with a curvature {curv}")
                        self.get_logger().info(f"yaw1 is: {yaw1}, yaw2 is: {yaw2}, yaw3 is: {yaw3}")
                        self.get_logger().info("Done")
                # self.get_logger().info("curv is: "+str(curv))
                # _,_,yaw = self.euler_from_quaternion(path[0].pose.orientation)
                # yaw = yaw*(180/math.pi)
                # self.get_logger().info(f"yaw1 is: {yaw1}, yaw2 is: {yaw2}, yaw3 is: {yaw3}")
                # self.get_logger().info("Done")
            except Exception as e:
                self.get_logger().info(str(e))



def main (args=None):
    rclpy.init(args=args)
    node=my_node()
    rclpy.spin(node)

    rclpy.shutdown()


if __name__=="__main__":
    main()


