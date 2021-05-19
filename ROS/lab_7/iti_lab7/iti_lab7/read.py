#!/usr/bin/env python3
with open("turtle_commands.csv","r") as file:
    content = file.readlines()
    values = content[13].split(',')
    print(values[0],values[1])