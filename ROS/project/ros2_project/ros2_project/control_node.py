#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from turtlesim.srv import SetPen
from turtlesim.srv import Kill
from geometry_msgs.msg import Twist
from turtlesim.msg import Pose
from my_msgsandsrvs.srv import PosTurt
from my_msgsandsrvs.srv import Arv
import numpy as np
from math import sqrt, atan2

class my_node(Node):
    def __init__(self):
        super().__init__("move_turtle_node")
        self.get_logger().info("Node is starting now")
        # self.create_timer(1/1,self.timer_call)
        # self.create_service(PosTurt, "position_of_2nd_turtle", self.srv_call)
        self.req_x = 0
        self.req_y = 0
        self.response = 0
        self.obj_vel = self.create_publisher(Twist,"/turtle1/cmd_vel",10)
        self.obj_pos = self.create_subscription(Pose,"/turtle1/pose",self.call_sub,10)
        self.obj_pos = 0
        self.arrive = False
        self.create_service(PosTurt, "position_of_2nd_turtle", self.srv_call)
        # self.obj_pos = self.create_subscription(Pose,"/turtle1/pose",self.call_sub,10)

        # msg = Twist()
        # msg.linear.x = 10.0
        # msg.linear.y = 5.0
        # # msg.linear.z = 0.0
        # msg.angular.x = 0.0
        # msg.angular.y = 0.0
        # msg.angular.z = 1.8
        # self.obj_vel.publish(msg)

    def srv_call(self,rq, rsp):
        self.req_x = rq.x
        self.req_y = rq.y
        # self.get_logger().info("flag_srv")
        # self.obj_pos = self.create_subscription(Pose,"/turtle1/pose",self.call_sub,10)
        # rsp.success = True
        # if self.arrive == True:
        #     rsp.success = True
        # else:
        #     rsp.success = False
        return rsp

    def call_sub(self,pos1):
        # self.linear_dist=abs(sqrt(((self.desierd_x-self.now_x)**2)+((self.desired_y-self.now_y)**2)))
        # self.lin_vel=self.linear_dist*self.P_lin
        # self.theta_desired=atan2((self.desired_y-self.now_y),(self.desierd_x-self.now_x))
        # self.theta_error=self.theta_desired-self.now_theta
        # self.get_logger().info("flag_sub")
        new = Twist() #0.5
        distance = 0.5*abs(np.sqrt((self.req_x-pos1.x)**2+(self.req_y-pos1.y)**2))
        theta = (atan2((self.req_y-pos1.y),(self.req_x-pos1.x)))
        if distance>0.2:
            new.linear.x = distance#10.0 #np.sqrt((self.req_x-pos1.x)**2)
            new.linear.y = 0.0#5.0 #(self.req_y-pos1.y)
            # new.linear.z = 0.0
            # new.angular.x = 0.0
            # new.angular.y = 0.0
            new.angular.z = 2.5*(theta-pos1.theta)
            # new.angular.z = atan(5.0/10.0)
            #self.get_logger().info(str(pos1.x)+str(pos1.y))
            self.obj_vel.publish(new)
            # self.arrive = False
        else:
            #self.get_logger().info(str(pos1.x)+str(pos1.y))
            # self.arrive = True
            # call client
            self.call_client(True)


    def call_client(self,arrived):
        client = self.create_client(Arv,"Arrival_of_turtle_1")
        while client.wait_for_service(0.5) == False:
            self.get_logger().warn("Wait for server node")
        
        request = Arv.Request()
        request.arrived = arrived

        future_obj = client.call_async(request)
        future_obj.add_done_callback(self.future_call)

    def future_call(self,future_msg):
        pass
        # self.get_logger().info("turtle1 is at position of turtle2")
        # self.call_client_3("turtle2")


        # msg = Pose()
        # msg.x = 2.0
        # msg.y = 0.0
        # msg.theta = 0.0
        # msg.linear_velocity = 1.0
        # msg.angular_velocity = 0.2
        # self.obj_pos.publish(msg)
        
        

    # def timer_call(self):
    #     msg = Twist()
    #     msg.linear.x = 2.0
    #     msg.linear.y = 0.0
    #     msg.linear.z = 0.0
    #     msg.angular.x = 0.0
    #     msg.angular.y = 0.0
    #     msg.angular.z = 1.8
    #     self.obj_pub.publish(msg)

    
 

def main(args=None):
    rclpy.init(args=args)
    node = my_node()
    rclpy.spin(node)

    rclpy.shutdown()

if __name__ == "__main__":
    main()