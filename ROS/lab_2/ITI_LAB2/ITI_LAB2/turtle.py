#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from example_interfaces.msg import String
from std_srvs.srv import Empty

class my_client(Node):
    def __init__(self):
        super().__init__("Client_turtle")
        self.srv_client()
    

    def srv_client(self):
        client = self.create_client(Empty,"reset")
        while client.wait_for_service(0.5) == False:
            self.get_logger().warn("Wait for server node")
        
        request = Empty.Request()

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