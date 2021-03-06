import json
from Raspi_PWM_Servo_Driver import PWM
from Raspi_MotorHAT import Raspi_MotorHAT, Raspi_DCMotor
import time
import requests
import serial as serial

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
  stats = []
  for i in r.json().items():
    stats.append(i[1])
  return stats

def checkShot():
    i = 0
    value = sensor.Measurement(trig_pin,
                            echo_pin,
                            unit='imperial',
                            round_to=2)
    while(i<500):
        raw = value.raw_distance(sample_size=1, sample_wait=0.01)
        
        imperial = value.distance_imperial(raw)
        print imperial < 4.00
        print imperial
        if(imperial<4):
            print "ballz"
            return 1
        i+=1
    return 0

def postShotResults(status):
  
  headers = {'content-type': 'application/json'}
  url = 'https://rllh3iqk97.execute-api.us-east-1.amazonaws.com/prod/turret?a=10'

  data = {"shotStatus": status}

  r =requests.post(url, data=json.dumps(data), headers=headers)
  requestStatus = r.json()['statusCode']
  if requestStatus != 200:
    print("Error!: " + str(r.json()))
    return False
  else:
    print("POST success")
    return True

def setSpeed(speed):
    motor.run(Raspi_MotorHAT.BACKWARD)
    motor.setSpeed(speed)

def resetMotors():
	motor.run(Raspi_MotorHAT.RELEASE)
        setAngle(0)

#[angle,speed]

def runTurret(x):
    setAngle(x[1])
    setSpeed(x[0])
    print "Speed set and angle"
    time.sleep(10)


def check_shot(x):
    runTurret(x)
    checkshot()
    try:
        print "here"
	s = str(int(ser.readline()))
        print s + "this"
    except:
	pass
    if(s):
	return(1)
    return(0)


def main():

    x = getShotStats()
    if x == []:
        print("No shot in queue")
        return

    result = check_shot(x)
    resetMotors()
    print result
    postShotResults(result)

main()
