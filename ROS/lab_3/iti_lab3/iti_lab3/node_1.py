#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from example_interfaces.msg import String
from example_interfaces.msg import Int64
from my_msgsandsrvs.msg import StrInt

class node_1(Node):
    def __init__(self):
        super().__init__("StrInt_publisher")
        self.get_logger().info("Pub node is starting now")
        self.num = 5
        self.obj_str_num = self.create_publisher(StrInt,"string_number",10)
        self.create_timer(1/1,self.timer_call) 

    def timer_call(self):
        str_num = StrInt()
        str_num.number = self.num
        str_num.message = f"Moaz is publishing: {self.num}"
        self.obj_str_num.publish(str_num)
        self.get_logger().info(str(self.num))

def main(args=None):
    rclpy.init(args=args)
    node = node_1()
    rclpy.spin(node)

    rclpy.shutdown()

if __name__ == "__main__":
    main()