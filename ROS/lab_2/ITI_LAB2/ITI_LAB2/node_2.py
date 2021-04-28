#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from example_interfaces.msg import String
from example_interfaces.msg import Int64
from example_interfaces.srv import SetBool

class node_2(Node):
    def __init__(self):
        super().__init__("number_counter")
        self.acc = 0
        # self.obj_num = self.create_publisher(Int64,"number",10)
        self.obj_pub = self.create_publisher(Int64,"number_counter",10)
        self.obj_sub = self.create_subscription(Int64,"number",self.call_1,10)
        self.create_service(SetBool, "number_counter_server", self.srv_call)
        self.get_logger().info("Sub node is starting now") 

    def call_1(self,msg):

        msg_num = Int64()
        msg_num.data = self.acc
        
        self.obj_pub.publish(msg_num)

        self.get_logger().info(str(self.acc))

        self.acc += msg.data
       
    def srv_call(self,rq,rsp):
        req_data = rq.data
        if req_data == True:
            rsp.message = "Counter is resetted"
            rsp.success = True
            self.acc = 0
            self.get_logger().info("Counter is resetting to 0")
            return rsp
        elif req_data == False:
            rsp.message = "Counter is continuous"
            rsp.success = False
            self.get_logger().info("Counter is continuing")
            return rsp
        # return rsp

def main(args=None):
    rclpy.init(args=args)
    node = node_2()
    rclpy.spin(node)

    rclpy.shutdown()

if __name__ == "__main__":
    main()