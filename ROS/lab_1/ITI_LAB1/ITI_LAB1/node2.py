#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from example_interfaces.msg import String

class node_2(Node):
    def __init__(self):
        super().__init__("number_counter")
        self.obj_num = self.create_publisher(String,"number",10)
        self.obj_2 = self.create_publisher(String,"reset_flag",10)
        self.obj_1 = self.create_subscription(String,"str_topic",self.call_1,10)
        self.get_logger().info("Node 2 is starting now") 

    def call_1(self,msg):
        '''
        s = msg.data
        #s = 'hi'
        self.get_logger().info(s.split(',')[-1])
        msg_p = String()
        msg_p.data = "reset"
        self.obj_2.publish(msg_p)
        '''
        if int(msg.data.split(',')[-1]) < 5:
            self.get_logger().info(msg.data)
            #msg_p = String()
            #msg_p.data = "go"
            #self.obj_2.publish(msg_p)
        elif int(msg.data.split(',')[-1]) == 5:
            self.get_logger().info(msg.data)
            msg_p = String()
            msg_p.data = "reset"
            self.obj_2.publish(msg_p)

def main(args=None):
    rclpy.init(args=args)
    node = node_2()
    rclpy.spin(node)

    rclpy.shutdown()

if __name__ == "__main__":
    main()