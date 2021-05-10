#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from example_interfaces.msg import String
# rclpy.qos.qos_profile_sensor_data
from rclpy.qos import qos_profile_sensor_data

class my_node(Node):
    def __init__(self):
        super().__init__("sub_task1")
        self.obj_sub = self.create_subscription(String,"/my_topic",self.sub_call,qos_profile_sensor_data)
        self.get_logger().info("Subscriber of task 1 is starting now")
        self.count = 0

    def sub_call(self,msg):
        self.get_logger().info(f"Moaz heard : {msg.data}, {self.count} times")
        self.count += 1

def main(args=None):
    rclpy.init(args=args)
    node = my_node()
    rclpy.spin(node)

    rclpy.shutdown()

if __name__ == "__main__":
    main()