import json
from Raspi_PWM_Servo_Driver import PWM
from Raspi_MotorHAT import Raspi_MotorHAT, Raspi_DCMotor
import time
import requests

pwm = PWM(0x06F)
mh = Raspi_MotorHAT(addr=0x6f)
motor = mh.getMotor(1)

servoMin = 0  # Min pulse length out of 4096
servoMax = 650  # Max pulse length out of 4096

def setAngle(angle):
    if angle > 45 or angle < 0:
        pwm.setPWM(1, 0, 0)
        print("error in angle number")
        return
    ticks = int(angle*5.55)+210
    if ticks < 210 or ticks > 460:
        pwm.setPWM(1, 0, 0)
        print("error in angle number")
        return
    pwm.setPWMFreq(50)
    pwm.setPWM(1, 0, ticks)

def getShotStats():
  r = requests.get('https://un3639u15a.execute-api.us-east-1.amazonaws.com/prod/turretGetSettings')
  stats =[]
  for i in r.json().items():
    stats.append(i[1])
  return stats

def setSpeed(speed):
    motor.setSpeed(25)
    motor.run(Raspi_MotorHAT.BACKWARD)
    time.sleep(1)
    motor.setSpeed(35)
    time.sleep(1)
    motor.setSpeed(200)

def resetMotors():
	motor.run(Raspi_MotorHAT.RELEASE)
        setAngle(0)

#[angle,speed]

def loop():
    x = getShotStats()
    print x
    setAngle(x[1])
    setSpeed(x[0])
    print "Speed set and angle"
    time.sleep(10)
    resetMotors()
loop()

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
