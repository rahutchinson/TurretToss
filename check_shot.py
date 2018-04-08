import serial
import time

def check_shot():
    ser = serial.Serial('/dev/ttyACM0',9600)
    s = None
    ser.write(bytes(b'1'))
	time.sleep(3)
	try:
		s = str(int (ser.readline()))	
	except:
		pass
	if(s):
		return(1)
	return(0)
