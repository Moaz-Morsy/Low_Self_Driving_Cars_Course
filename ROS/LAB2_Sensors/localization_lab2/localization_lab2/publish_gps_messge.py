#!/usr/bin/env python3
import rclpy
import csv
from rclpy.node import Node
from rclpy.qos import QoSProfile
#TODO Import needed messages
from sensor_msgs.msg import NavSatFix
from math import sin, cos, pi
import numpy as np


class my_node (Node):
    def __init__(self):
        super().__init__("Node_name")
        self.get_logger().info("Node is started")
        qos_profile = QoSProfile(depth=10) 
        self.csv_file_path = "/home/moaz/ROS_WS/src/localization_lab2/localization_lab2/GGA_GST.csv"
        self.lines = []
        with open(self.csv_file_path, newline='\n') as csvfile:       
          self.readCSV = csv.reader(csvfile, delimiter = ',')
          for row in self.readCSV:
              self.lines.append(row)

        self.count = 1 #Skip header

        #TODO create timer_call with the required frequency & publisher
        self.fix_pub=self.create_publisher(NavSatFix,"/fix",qos_profile)
        self.gps_msg = NavSatFix()
        self.gps_msg.header.frame_id= "gps_link"
        self.create_timer(1/5,self.timer_call)


    def timer_call(self):
        # self.gps_msg = NavSatFix()
        # self.gps_msg.header.frame_id = "gps_link"
        self.gps_msg.header.stamp = self.get_clock().now().to_msg()
        row = self.lines[self.count]
        self.get_logger().info(f"row {self.count}")
        self.count +=1
        if (self.count >= len(self.lines)): # repeat csv file continously
            self.count = 0

        #TODO get The following values from csv
        latitude_value =  row[2] #TODO 
        latitude_direction = row[3] #TODO 
        
        longitude_value = row[4] #TODO 
        longitude_direction = row[5] #TODO 

        altitude_value =  row[9] #TODO 

        # The following functions convert the string data in degrees/minutes to float data in degrees as ROS message requires.        
        latitude = self.convert_latitude(latitude_value, latitude_direction)
        longitude = self.convert_longitude(longitude_value, longitude_direction)
        altitude = self.safe_float(altitude_value)
        
        hdop = float(row[8]) #TODO 
        lat_std_dev = float(row[21]) #TODO 
        lon_std_dev = float(row[22]) #TODO 
        alt_std_dev = float(row[23]) #TODO 

        #TODO Fill the gps message and publish
        self.gps_msg.latitude = latitude
        self.gps_msg.longitude = longitude
        self.gps_msg.altitude = altitude
        self.gps_msg.position_covariance[0] = (hdop * lon_std_dev) ** 2
        self.gps_msg.position_covariance[4] = (hdop * lat_std_dev) ** 2
        self.gps_msg.position_covariance[8] = (2 * hdop * alt_std_dev) ** 2
        self.fix_pub.publish(self.gps_msg)



    def convert_latitude(self, field_lat, lat_direction):
        latitude = self.safe_float(field_lat[0:2]) + self.safe_float(field_lat[2:]) / 60.0
        if lat_direction == 'S':
            latitude = -latitude
        return latitude

    def convert_longitude(self, field_long, long_direction):
        longitude = self.safe_float(field_long[0:2]) + self.safe_float(field_long[2:]) / 60.0 
        if long_direction == 'W':
            longitude = -longitude
        return longitude

    def safe_float(self, field):
        try:
            return float(field)
        except ValueError:
            return float('NaN')
        
def main (args=None):
    rclpy.init(args=args)
    node=my_node()
    rclpy.spin(node)

    rclpy.shutdown()


if __name__=="__main__":
    main()
