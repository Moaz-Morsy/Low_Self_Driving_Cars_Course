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
from math import sqrt, atan2, pi
from rclpy.qos import qos_profile_sensor_data

class my_node(Node):
    def __init__(self):
        super().__init__("control_node")
        self.get_logger().info("Node is starting now")
        self.req_x = 0
        self.req_y = 0
        self.name = ""
        self.turtles = []
        self.start_time = self.get_clock().now().nanoseconds*(10**-9)
        # print(self.get_clock().now().nanoseconds)
        self.last_distance = 0
        self.last_error_theta = 0
        self.cum_error_dist = 0
        self.cum_error_theta = 0
        self.create_service(PosTurt, "position_of_2nd_turtle", self.srv_call)
        self.obj_vel = self.create_publisher(Twist,"/turtle1/cmd_vel",10)
        self.obj_pos = self.create_subscription(Pose,"/turtle1/pose",self.call_sub,10)
        self.obj_pos
        # self.create_service(PosTurt, "position_of_2nd_turtle", self.srv_call)


    def srv_call(self,rq, rsp):
        self.req_x = rq.x
        self.req_y = rq.y
        self.name = rq.name
        self.turtles.append((rq.name,rq.x,rq.y))
        return rsp

    def call_sub(self,pos1):
        # self.linear_dist=abs(sqrt(((self.desierd_x-self.now_x)**2)+((self.desired_y-self.now_y)**2)))
        # self.lin_vel=self.linear_dist*self.P_lin
        # self.theta_desired=atan2((self.desired_y-self.now_y),(self.desierd_x-self.now_x))
        # self.theta_error=self.theta_desired-self.now_theta
        # self.get_logger().info("start_sub")
        new = Twist() #0.5
        # distance = abs(np.sqrt((self.req_x-pos1.x)**2+(self.req_y-pos1.y)**2))
        # theta = (atan2((self.req_y-pos1.y),(self.req_x-pos1.x)))
        if self.turtles != []:
            # print(self.turtles)
            distance = abs(np.sqrt((self.turtles[0][1]-pos1.x)**2+(self.turtles[0][2]-pos1.y)**2))
            theta = (atan2((self.turtles[0][2]-pos1.y),(self.turtles[0][1]-pos1.x)))
            theta_diff =  (theta-pos1.theta)

            if theta_diff > (pi):
                theta_diff -= (2*pi)
            elif theta_diff < -(pi):
                theta_diff += (2*pi)

            self.end_time = self.get_clock().now().nanoseconds*(10**-9)

            rate_error_dist = (distance-self.last_distance)/(self.end_time-self.start_time)
            rate_error_theta = (theta_diff-self.last_error_theta)/(self.end_time-self.start_time)
            self.cum_error_dist += distance*(self.end_time-self.start_time)
            self.cum_error_theta += theta_diff*(self.end_time-self.start_time)
            
            PID_dist = (1*distance)+(0.00005*self.cum_error_dist)+(0.1*rate_error_dist)
            PID_theta =  (5*theta_diff)+(0.00005*self.cum_error_theta)+(0.1*rate_error_theta)

            self.get_logger().info(f"PID_dist {1*distance}, {0.00005*self.cum_error_dist}, {0.1*rate_error_dist}")
            self.get_logger().info(f"PID_theta theta_diff: {theta_diff} kp {5*theta_diff}, ki {0.00005*self.cum_error_theta}, kd {0.1*rate_error_theta}")
            
            if distance>0.1:
                new.linear.x = PID_dist
                new.angular.z = PID_theta
                self.start_time = self.end_time
                self.last_distance = distance
                self.last_error_theta = theta_diff
                # self.get_logger().info(str(distance))
                # self.get_logger().info(str(theta-pos1.theta))
                self.obj_vel.publish(new)
                #self.call_client(False)
            else:
                # self.get_logger().info(str(pos1.x)+str(pos1.y))
                # call client
                self.call_client(True, self.turtles[0][0])
                self.turtles.pop(0)
    
    def call_client(self,arrived,name):
        client = self.create_client(Arv,"Arrival_of_turtle_1")
        while client.wait_for_service(0.5) == False:
            self.get_logger().warn("Wait for server node")
        
        request = Arv.Request()
        request.arrived = arrived
        request.name = name

        future_obj = client.call_async(request)
        future_obj.add_done_callback(self.future_call)

    def future_call(self,future_msg):
        # pass
        self.get_logger().info(str(future_msg.result()))





def main(args=None):
    rclpy.init(args=args)
    node = my_node()
    rclpy.spin(node)

    rclpy.shutdown()

if __name__ == "__main__":
    main()