#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from turtlesim.srv import Spawn
from my_msgsandsrvs.srv import PosTurt
from my_msgsandsrvs.srv import Arv
from turtlesim.srv import Kill
from std_srvs.srv import Empty
import random


class my_client(Node):
    def __init__(self):
        super().__init__("Client_turtle")
        self.x = float(random.randint(1,10))
        self.y = float(random.randint(1,10))
        self.call_client_1(self.x,self.y)
        self.call_client_2(self.x,self.y)
        self.name = ''
        # self.x = 10.0
        # self.y = 5.0
        # self.call_client_1(self.x,self.y,0.0)
        # self.call_client_2(self.x,self.y)
        self.create_service(Arv,"Arrival_of_turtle_1", self.srv_call)
        # self.call_client_3("turtle2")
        # self.create_timer(1/100,self.timer_call)

    # def timer_call(self):
        # x = np.random.randint(1,11,size=1)
        # y = np.random.randint(1,11,size=1)
        # self.srv_client(float(x),float(y),0.0)
        # self.call_client_1(10.0,5.0,0.0)
        # self.call_client_2(10.0,5.0)

    def call_client_1(self,x,y):
        client = self.create_client(Spawn,"spawn")
        while client.wait_for_service(0.1) == False:
            self.get_logger().warn("Wait for server node")
        
        request = Spawn.Request()
        request.x = x
        request.y = y
        # request.theta = theta
        #request.name = name

        future_obj = client.call_async(request)
        # self.get_logger().info("hi there 1")
        future_obj.add_done_callback(self.future_call_1)

    def future_call_1(self,future_msg):
        self.name = future_msg.result().name
        self.get_logger().info(self.name)
        #self.call_client_2(10.0,5.0)

    def call_client_2(self,x,y):
        client = self.create_client(PosTurt,"position_of_2nd_turtle")
        while client.wait_for_service(0.5) == False:
            self.get_logger().warn("Wait for server node")
        
        request = PosTurt.Request()
        request.x = x
        request.y = y

        self.get_logger().info("hi there spawn")

        future_obj = client.call_async(request)
        # self.get_logger().info("hi there spawn")
        future_obj.add_done_callback(self.future_call_2)

    def future_call_2(self,future_msg):
        pass
        # self.get_logger().info(str(True))
        # if future_msg.result().success:
        #     self.get_logger().info(str(future_msg.result().success))
        #     self.get_logger().info("turtle1 has been arrived")
        #     self.call_client_3("turtle2")
        #     # self.x = random.randint(1,11)
        #     # self.y = random.randint(1,11)
        #     # self.call_client_1(float(self.x),float(self.y),0.0)
        #     # self.call_client_2(float(self.x),float(self.y))
        # else:
        #     self.get_logger().info(str(future_msg.result().success))
        #     self.get_logger().info("turtle1 is not there")
        #     self.call_client_2(self.x,self.y)
            # self.call_client_2(10.0,5.0)
            # self.call_client_2(float(self.x),float(self.y))
        # self.call_client_1(0.0,0.0,0.0)
        # if future_msg.result().success:

    
    def srv_call(self,rq,rsp):
        req = rq.arrived
        # if req:
        self.call_client_3(self.name)
        self.call_client_4()
        rsp.success = True
        # self.x = 1.0
        # self.y = 1.0
        self.x = float(random.randint(1,11))
        self.y = float(random.randint(1,11))
        self.call_client_1(self.x,self.y)
        self.call_client_2(self.x,self.y)
        self.get_logger().info("hi there srv")
        # rsp.success = True
    # rsp.success = True
        return rsp
    
    def call_client_3(self,name):
        client = self.create_client(Kill,"kill")
        while client.wait_for_service(0.5) == False:
            self.get_logger().warn("Wait for server node")
        
        request = Kill.Request()
        request.name = name

        future_obj = client.call_async(request)
        # self.get_logger().info("hi there 3")
        future_obj.add_done_callback(self.future_call_3)

    def future_call_3(self,future_msg):
        pass
        # self.get_logger().info("kill turtle")
        # self.x = float(random.randint(1,10))
        # self.y = float(random.randint(1,10))
        # self.call_client_1(self.x,self.y)
        # self.call_client_2(self.x,self.y)

    def call_client_4(self):
        client = self.create_client(Empty,"clear")
        while client.wait_for_service(0.5) == False:
            self.get_logger().warn("Wait for server node")
        
        request = Empty.Request()

        future_obj = client.call_async(request)
        # self.get_logger().info("hi there 4")
        future_obj.add_done_callback(self.future_call_4)

    def future_call_4(self,future_msg):
        pass
        # self.get_logger().info(str(future_msg.result()))
        



def main(args=None):
    rclpy.init(args=args)
    node = my_client()
    rclpy.spin(node)

    rclpy.shutdown()

if __name__ == "__main__":
    main()