#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from turtlesim.srv import Spawn
from my_msgsandsrvs.srv import PosTurt
from my_msgsandsrvs.srv import Arv
from turtlesim.srv import Kill
from std_srvs.srv import Empty
import random
# import time


class my_client(Node):
    def __init__(self):
        super().__init__("spawn_node")
        # self.x = float(random.randint(1,10))
        # self.y = float(random.randint(1,10))
        # self.spawn_call(self.x,self.y)
        # self.my_call(self.x,self.y)
        # self.name = ''
        # self.x = 10.0
        # self.y = 5.0
        # self.spawn_call(self.x,self.y,0.0)
        # self.my_call(self.x,self.y)
        self.create_service(Arv,"Arrival_of_turtle_1", self.srv_call)

        self.create_timer(3/1,self.timer_call)

    def timer_call(self):
        self.x = float(random.randint(1,10))
        self.y = float(random.randint(1,10))
        self.spawn_call(self.x,self.y)
        # self.my_call(self.x,self.y,self.name)
        self.get_logger().warn("new turtle is added")

    def spawn_call(self,x,y):
        client = self.create_client(Spawn,"spawn")
        while client.wait_for_service(0.1) == False:
            self.get_logger().warn("Wait for server node")
        
        request = Spawn.Request()
        request.x = x
        request.y = y
        # request.theta = theta
        # request.name = name

        future_obj = client.call_async(request)
        self.get_logger().info("hi there spawn_call")
        future_obj.add_done_callback(self.spawn_future_call)

    def spawn_future_call(self,future_msg):
        self.name = future_msg.result().name
        self.get_logger().info(self.name)
        self.my_call(self.x,self.y,self.name)

    def my_call(self,x,y,name):
        client = self.create_client(PosTurt,"position_of_2nd_turtle")
        while client.wait_for_service(0.5) == False:
            self.get_logger().warn("Wait for server node")
        
        request = PosTurt.Request()
        request.x = x
        request.y = y
        request.name = name

        # self.get_logger().info("hi there my_call")

        future_obj = client.call_async(request)
        future_obj.add_done_callback(self.my_future_call)

    def my_future_call(self,future_msg):
        # pass
        self.get_logger().info(str(future_msg.result()))

    
    def srv_call(self,rq,rsp):
        # self.get_logger().info("hi there srv_call")
        if rq.arrived == True:
            self.get_logger().info("Arrival")
            self.kill_call(rq.name)
            self.get_logger().info("turtle killed")
            self.clear_call()
            # self.x = float(random.randint(1,11))
            # self.y = float(random.randint(1,11))
            # self.spawn_call(self.x,self.y)
            # self.my_call(self.x,self.y)
            rsp.success = True
        return rsp
        # else:
        #     #self.my_call(self.x,self.y)
        #     rsp.success = False
        #     return rsp
    
    def kill_call(self,name):
        client = self.create_client(Kill,"kill")
        while client.wait_for_service(0.5) == False:
            self.get_logger().warn("Wait for server node")
        
        request = Kill.Request()
        request.name = name

        self.get_logger().info("inside kill func")

        future_obj = client.call_async(request)
        # self.get_logger().info("hi there kill_call")
        future_obj.add_done_callback(self.kill_future_call)

    def kill_future_call(self,future_msg):
        # pass
        self.get_logger().info(str(future_msg.result()))
        # self.get_logger().info("kill turtle")
        # self.x = float(random.randint(1,10))
        # self.y = float(random.randint(1,10))
        # self.spawn_call(self.x,self.y)
        # self.my_call(self.x,self.y)

    def clear_call(self):
        client = self.create_client(Empty,"clear")
        while client.wait_for_service(0.5) == False:
            self.get_logger().warn("Wait for server node")
        
        request = Empty.Request()

        future_obj = client.call_async(request)
        # self.get_logger().info("hi there clear_call")
        future_obj.add_done_callback(self.clear_future_call)

    def clear_future_call(self,future_msg):
        # pass
        self.get_logger().info(str(future_msg.result()))
        # self.x = float(random.randint(1,11))
        # self.y = float(random.randint(1,11))
        # self.spawn_call(self.x,self.y)
        # self.my_call(self.x,self.y)
        # self.get_logger().info(str(future_msg.result()))
        



def main(args=None):
    rclpy.init(args=args)
    node = my_client()
    rclpy.spin(node)

    rclpy.shutdown()

if __name__ == "__main__":
    main()