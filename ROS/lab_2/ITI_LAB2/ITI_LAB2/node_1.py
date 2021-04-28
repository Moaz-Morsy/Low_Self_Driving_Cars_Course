#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from example_interfaces.msg import String
from example_interfaces.msg import Int64
# from example_interfaces.srv

class node_1(Node):
    def __init__(self):
        super().__init__("Int_publisher")
        self.get_logger().info("Pub node is starting now")
        self.num = 3
        self.obj_num = self.create_publisher(Int64,"number",10)
        self.create_timer(1/1,self.timer_call) 

    def timer_call(self):
        msg_num = Int64()
        msg_num.data = self.num
        self.obj_num.publish(msg_num)
        self.get_logger().info(str(self.num))

def main(args=None):
    rclpy.init(args=args)
    node = node_1()
    rclpy.spin(node)

    rclpy.shutdown()

if __name__ == "__main__":
    main()