#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from std_srvs.srv import Empty
from turtlesim.msg import Pose
from rclpy.qos import qos_profile_sensor_data
class my_client(Node):
    def __init__(self):
        super().__init__("Client_turtle")
        self.obj_pos = self.create_subscription(Pose,"/turtle1/pose",self.call_sub,qos_profile_sensor_data)
        # self.srv_client()
    

    def srv_client(self):
        client = self.create_client(Empty,"reset")
        while client.wait_for_service(0.5) == False:
            self.get_logger().warn("Wait for server node")
        
        request = Empty.Request()

        future_obj = client.call_async(request)
        future_obj.add_done_callback(self.future_call)

    def future_call(self,future_msg):
        self.get_logger().info(str(future_msg.result()))

    def call_sub(self,pos):
        if (pos.x<2 or pos.x>8) or (pos.y<2 or pos.y>8):
            self.get_logger().info("turtle has crossed its limits, it will be reset")
            self.srv_client()
        # else:
        #     self.get_logger().info("turtle is ok")

def main(args=None):
    rclpy.init(args=args)
    node = my_client()
    rclpy.spin(node)

    rclpy.shutdown()

if __name__ == "__main__":
    main()