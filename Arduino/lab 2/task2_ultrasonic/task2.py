import serial
import time
import datetime as dt
import matplotlib.pyplot as plt
import matplotlib.animation as animation



serialcomm = serial.Serial("/dev/ttyACM1","9600")
serialcomm.timeout = 1

# Create figure for plotting
fig = plt.figure()
ax = fig.add_subplot(1, 1, 1)
xs = []
ys = []

# This function is called periodically from FuncAnimation
def animate(i, xs, ys):
	# time.sleep(0.5)
	try:
		distance = serialcomm.readline().decode('ascii')
		distance_incm = float(distance.split()[-1])
		# print(serialcomm.readline().decode('ascii'))
		# print(distance_incm) 
		print(f"Distance in cm: {distance_incm}, Distance in inch: {distance_incm/2.54} ")
		x = distance_incm

		# Add x and y to lists
		xs.append(dt.datetime.now().strftime('%H:%M:%S.%f'))
		ys.append(x)

		# Limit x and y lists to 20 items
		xs = xs[-20:]
		ys = ys[-20:]

		# Draw x and y lists
		ax.clear()
		ax.plot(xs, ys)

		# Format plot
		plt.xticks(rotation=45, ha='right')
		plt.subplots_adjust(bottom=0.30)
		plt.title('Distance Vs Time')
		plt.ylabel('Distance (cm)')
	except Exception as e:
		pass
	
# Set up plot to call animate() function periodically
ani = animation.FuncAnimation(fig, animate, fargs=(xs, ys), interval=10)
plt.show()

# while True:
# 	time.sleep(0.5)
# 	try:
# 		distance = serialcomm.readline().decode('ascii')
# 		distance_incm = float(distance.split()[-1])
# 		# print(serialcomm.readline().decode('ascii'))
# 		# print(distance_incm) 
# 		print(f"Distance in cm: {distance_incm}, Distance in inch: {distance_incm/2.54} ")
# 	except Exception as e:
# 		# print(e)
# 		continue
	
serialcomm.close()


	




