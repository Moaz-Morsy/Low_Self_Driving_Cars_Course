#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from example_interfaces.msg import String
from example_interfaces.msg import Int64
from example_interfaces.srv import SetBool

class node_3(Node):
    def __init__(self):
        super().__init__("reset_client")
        self.get_logger().warn("Client node is starting now")
        self.srv_client(True)

    def srv_client(self,data):
        client = self.create_client(SetBool,"number_counter_server")
        # self.get_logger().warn("Ok call")
        while client.wait_for_service(0.5) == False:
            self.get_logger().warn("Ok call")
        
        request = SetBool.Request()
        request.data = data

        future_obj = client.call_async(request)
        future_obj.add_done_callback(self.future_call)

    def future_call(self,future_msg):
        if future_msg.result().success:
            self.get_logger().info(future_msg.result().message)

def main(args=None):
    rclpy.init(args=args)
    node = node_3()
    rclpy.spin(node)

    rclpy.shutdown()

if __name__ == "__main__":
    main()