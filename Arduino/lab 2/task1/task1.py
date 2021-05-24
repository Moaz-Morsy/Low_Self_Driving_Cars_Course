#! /usr/bin/python3
lines = []
with open('python_test_file.txt', 'r') as file:
    for line in file:
        values = line.strip("\n").split(",   ")
        # if values[-1]!='     ':
        try:
            v1, v2, v3 = float(values[-3]), float(values[-2]), float(values[-1])
            lines.append(line.strip("\n")+",speed,   "+str(v1**2+v2**2+v3**2)+"\n")
        except:
            continue
        # lines.append(line.strip("\n").split(",   "))

# print(lines[-1])
with open('new_python_test_file.txt', 'w') as new_file:
    new_file.writelines(lines)