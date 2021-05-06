#!/usr/bin/env python3

from math import sin, cos, pi
import rclpy
from rclpy.node import Node
from rclpy.qos import QoSProfile
from geometry_msgs.msg import Quaternion
from sensor_msgs.msg import JointState
from tf2_ros import TransformBroadcaster, TransformStamped

class StatePublisher(Node):

    def __init__(self):
        rclpy.init()
        super().__init__('state_publisher')

        qos_profile = QoSProfile(depth=10)
        self.broadcaster = TransformBroadcaster(self, qos=qos_profile)
        self.nodeName = self.get_name()
        self.get_logger().info("{0} started".format(self.nodeName))

        degree = pi / 180.0
        angle = 30#pi/6.0
        start = 30#pi/6.0
        end = -30#-pi/6.0
        cond = True
        loop_rate = self.create_rate(10)

        # message declarations
        servo_trans = TransformStamped()
        servo_trans.header.frame_id = 'servo_link'
        servo_trans.child_frame_id = 'lidar_link'

        try:
            while rclpy.ok():
                rclpy.spin_once(self)

                now = self.get_clock().now()

                # update transform
                servo_trans.transform.rotation = \
                    euler_to_quaternion(0, angle*degree, 0) # roll,pitch,yaw

                # send the joint state and transform
                self.broadcaster.sendTransform(servo_trans)

                # Create new robot state
                if  cond and (angle<=start):
                    angle -= 1
                    if angle == end:
                        cond = False 
                elif angle>=end:
                    angle += 1
                    if angle == start:
                        cond = True

                # This will adjust as needed per iteration
                loop_rate.sleep()

        except KeyboardInterrupt:
            pass

def euler_to_quaternion(roll, pitch, yaw):
    qx = sin(roll/2) * cos(pitch/2) * cos(yaw/2) - cos(roll/2) * sin(pitch/2) * sin(yaw/2)
    qy = cos(roll/2) * sin(pitch/2) * cos(yaw/2) + sin(roll/2) * cos(pitch/2) * sin(yaw/2)
    qz = cos(roll/2) * cos(pitch/2) * sin(yaw/2) - sin(roll/2) * sin(pitch/2) * cos(yaw/2)
    qw = cos(roll/2) * cos(pitch/2) * cos(yaw/2) + sin(roll/2) * sin(pitch/2) * sin(yaw/2)
    return Quaternion(x=qx, y=qy, z=qz, w=qw)

def main():
    node = StatePublisher()

if __name__ == '__main__':
    main()

