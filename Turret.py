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
    pwm.setPWMFreq(60)
    pwm.setPWM(0, 0, angle*2)

def getShotStats():
  r = requests.get('https://un3639u15a.execute-api.us-east-1.amazonaws.com/prod/turretGetSettings')
  stats =[]
  for i in r.json().items():
    stats.append(i[1])
  return stats

def setSpeed(speed):
    motor.setSpeed(speed)
    motor.run(Raspi_MotorHAT.FORWARD)

def turnOffMotors():
	motor.run(Raspi_MotorHAT.RELEASE)

#[angle,speed]

def loop():
    x = getShotStats()
    print x
    setAngle(x[1])
    setSpeed(x[0])
    print "Speed set and angle"
    time.sleep(2)
    turnOffMotors()
    setAngle(10)

loop()
