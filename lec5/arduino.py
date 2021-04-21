import serial
import time

serialcomm = serial.Serial('/dev/ttyACM0','9600')
serialcomm.timeout = 1

while True:

	input_user = input("Enter Input : ").strip()
	
	if input_user == "Done":
		print("finished")
		break
	
	serialcomm.write(input_user.encode())
	
	
	time.sleep(0.5)
	
	print(serialcomm.readline().decode('ascii'))
	
	
serialcomm.close()


	




