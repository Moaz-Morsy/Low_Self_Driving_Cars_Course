#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from turtlesim.msg import Pose
from rclpy.qos import qos_profile_sensor_data
class my_node(Node):
    def __init__(self):
        super().__init__("sub_task2")
        self.obj_pub = self.create_subscription(Pose,"/turtle1/custom_pose",self.timer_call,qos_profile_sensor_data)
        self.get_logger().info("Subscriber of task 2 is starting now")

    def timer_call(self,pos):
        print(pos.x ,",", pos.y)
        # print(pos.y)

def main(args=None):
    rclpy.init(args=args)
    node = my_node()
    rclpy.spin(node)

    rclpy.shutdown()

if __name__ == "__main__":
    main()