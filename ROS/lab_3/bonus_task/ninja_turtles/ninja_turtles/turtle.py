#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from example_interfaces.msg import String
from turtlesim.srv import Spawn

class my_client(Node):
    def __init__(self):
        super().__init__("Client_turtle")
        self.srv_client(4.0,8.0,0.0,"moaz")
        #self.create_timer(1/1,self.timer_call)

    # def timer_call(self):
    #     self.srv_client(float(input("Enter x: ")),
    #     float(input("Enter y: ")),float(input("Enter theta: ")),
    #     input("Enter name: "))

    def srv_client(self,x,y,theta,name):
        client = self.create_client(Spawn,"spawn")
        while client.wait_for_service(0.5) == False:
            self.get_logger().warn("Wait for server node")
        
        request = Spawn.Request()
        request.x = x
        request.y = y
        request.theta = theta
        request.name = name

        future_obj = client.call_async(request)
        future_obj.add_done_callback(self.future_call)

    def future_call(self,future_msg):
        self.get_logger().info(str(future_msg.result()))

def main(args=None):
    rclpy.init(args=args)
    node = my_client()
    rclpy.spin(node)

    rclpy.shutdown()

if __name__ == "__main__":
    main()