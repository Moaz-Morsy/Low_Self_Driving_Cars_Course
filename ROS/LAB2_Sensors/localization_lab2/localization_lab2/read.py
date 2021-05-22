#!/usr/bin/env python3
import csv
csv_file_path = "/home/moaz/ROS_WS/src/localization_lab2/localization_lab2/GGA_GST.csv"
lines = []
with open(csv_file_path, newline='\n') as csvfile:       
    readCSV = csv.reader(csvfile, delimiter = ',')
    for row in readCSV:
        lines.append(row)

print(lines[1])