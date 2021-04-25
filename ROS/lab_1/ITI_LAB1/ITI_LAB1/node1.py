#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from example_interfaces.msg import String

class node_1(Node):
    def __init__(self):
        self.count = 0
        super().__init__("str_publisher")
        self.create_timer(1/1,self.timer_call)
        self.obj_1 = self.create_publisher(String,"str_topic",10)
        self.obj_2 = self.create_subscription(String,"reset_flag",self.call_2,10)
        self.get_logger().info("Node 1 is starting now")

    def timer_call(self):
        msg = String()
        msg.data = f"Moaz is publishing , {self.count}"
        self.obj_1.publish(msg)
        self.count += 1

    def call_2(self,msg):
        if msg.data == "reset":
            self.get_logger().info(msg.data)
            self.count = 0
        else:
            self.get_logger().info(msg.data)
            
 

def main(args=None):
    rclpy.init(args=args)
    node = node_1()
    rclpy.spin(node)

    rclpy.shutdown()

if __name__ == "__main__":
    main()