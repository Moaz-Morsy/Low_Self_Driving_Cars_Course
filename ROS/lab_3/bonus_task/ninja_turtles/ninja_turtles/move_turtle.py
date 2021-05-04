#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from example_interfaces.msg import String
from geometry_msgs.msg import Twist

class my_node(Node):
    def __init__(self):
        super().__init__("move_turtle_node")
        self.get_logger().info("Node is starting now")
        self.flag = 0
        self.create_timer(1/1,self.timer_call)
        self.obj_pub = self.create_publisher(Twist,"/turtle1/cmd_vel",10)

    def timer_call(self):
        if self.flag == 0:
            msg = Twist()
            msg.linear.x = 2.0
            msg.linear.y = 0.0
            msg.linear.z = 0.0
            self.flag += 1
            self.obj_pub.publish(msg)
        elif self.flag == 1:
            msg = Twist()
            msg.linear.x = 2.0
            msg.linear.y = 0.0
            msg.linear.z = 0.0
            msg.angular.x = 0.0
            msg.angular.y = 0.0
            msg.angular.z = 1.8
            self.flag += 1
            self.obj_pub.publish(msg)
        elif self.flag == 2:
            msg = Twist()
            msg.angular.x = 0.0
            msg.angular.y = 0.0
            msg.angular.z = 1.8
            self.flag = 0
            self.obj_pub.publish(msg)
    
 

def main(args=None):
    rclpy.init(args=args)
    node = my_node()
    rclpy.spin(node)

    rclpy.shutdown()

if __name__ == "__main__":
    main()