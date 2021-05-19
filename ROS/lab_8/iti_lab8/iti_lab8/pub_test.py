#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from example_interfaces.msg import String

class my_node(Node):
    def __init__(self):
        super().__init__("my_node")
        # self.create_timer(1/1,self.timer_call)
        self.obj_pub = self.create_publisher(String,"my_topic",10)
        self.get_logger().info("Publisher is starting now")
        self.str = "Hi"
        self.create_timer(1/1,self.timer_call)
        # self.str = "Hello"

    def timer_call(self):
        msg = String()
        if self.str == "Hi":
            msg.data = self.str
            self.str =  "Hello"
            self.obj_pub.publish(msg)
        elif self.str == "Hello":
            msg.data = self.str
            self.str =  "Hi"
            self.obj_pub.publish(msg) 

def main(args=None):
    rclpy.init(args=args)
    node = my_node()
    rclpy.spin(node)

    rclpy.shutdown()

if __name__ == "__main__":
    main()