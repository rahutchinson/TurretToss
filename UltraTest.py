from hcsr04sensor import sensor
import time


trig_pin = 23
echo_pin = 24

def main():
    i = 0
    value = sensor.Measurement(trig_pin,
                            echo_pin,
                            unit='imperial',
                            round_to=2)
    while(i<500):
        raw = value.raw_distance(sample_size=1, sample_wait=0.01)
        
        imperial = value.distance_imperial(raw)
        print imperial is int
        print imperial < 4.00
        print imperial
        if(imperial<4):
            print "ballz"
            break
        i+=1


def test():
    value = sensor.Measurement(trig_pin, echo_pin)
    raw = value.raw_distance()

    imperial = value.distance_imperial(raw)

    print imperial

if __name__ == "__main__":
    main()
