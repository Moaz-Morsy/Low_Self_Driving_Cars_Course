#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from std_srvs.srv import Empty
from turtlesim.msg import Pose
from geometry_msgs.msg import Twist
from rclpy.qos import QoSProfile
class my_node(Node):
    def __init__(self):
        super().__init__("move_turtle")
        self.get_logger().info("Moving turtle is starting now")
        qos_profile = QoSProfile(depth=10)
        self.line = 1
        with open("/home/moaz/ROS_WS/src/iti_lab7/iti_lab7/turtle_commands.csv","r") as file:
            self.content = file.readlines()
        self.obj_vel = self.create_publisher(Twist,"/turtle1/cmd_vel",qos_profile)
        self.obj_pos = self.create_subscription(Pose,"/turtle1/pose",self.sub_call,qos_profile)
        self.create_timer(1/1,self.timer_call_2)
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

    def sub_call(self,pos):
        if (pos.x<2 or pos.x>8) or (pos.y<2 or pos.y>8):
            self.get_logger().info("turtle has crossed its limits, it will be reset")
            self.srv_client()
        # else:
        #     self.get_logger().info("turtle is ok")

    def timer_call_1(self):
        if self.line <= 12:
            values = self.content[self.line].split(',')
            vel = Twist()
            vel.linear.x = float(values[0])
            vel.angular.z = float(values[1])
            self.obj_vel.publish(vel)
            self.line += 1
        else:
            self.get_logger().info("Done")
    
    def timer_call_2(self):
        try:
            values = self.content[self.line].split(',')
            vel = Twist()
            vel.linear.x = float(values[0])
            vel.angular.z = float(values[1])
            self.obj_vel.publish(vel)
            self.line += 1
        except Exception as e:
            self.get_logger().info(str(e))
            self.get_logger().info("Done")

def main(args=None):
    rclpy.init(args=args)
    node = my_node()
    rclpy.spin(node)

    rclpy.shutdown()

if __name__ == "__main__":
    main()