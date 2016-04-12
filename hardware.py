import RPi.GPIO as GPIO
GPIO.setmode( GPIO.BCM )

def cleanup():
    GPIO.cleanup()

class Curtain():

    def __init__( s, servo=18, encoder=(23,24) ):
        s.initservo( servo )
        s.initencoder( encoder )

    def initservo( s, pin ):
        s.setservo()
        GPIO.setup( pin, GPIO.OUT )
        s.pwm = GPIO.PWM( pin, s.duty )

    def setservo( s, duty=50, mid=7.9, high=9.3, low=6.7 ):
        s.duty = duty
        s.dc = ( mid, high, low )
        s.engaged = False

    def initencoder( s, pins ):
        s.setencoder()
        s.encpin = pins

        GPIO.setup( pins, GPIO.IN, GPIO.PUD_UP )
        for p in pins:
            GPIO.add_event_detect( p, GPIO.BOTH, callback=s.encoder_interrupt )

    def setencoder( s, limits=(0,500) ):
        s.penc = 0
        s.pos = 0
        s.limits = limits

    def encoder_interrupt( s, c ):
        enc = sum( 1<<i for i in (0,1) if GPIO.input(s.encpin[i]) == GPIO.HIGH )
        s.pos += ((0,1,-1,0),(-1,0,0,1),(1,0,0,-1),(0,-1,1,0))[s.penc][enc]
        s.penc = enc

    def position( s ):
        return s.limits[0] + float(s.pos)/( s.limits[1] - s.limits[0] )

    def engage( s ):
        if not s.engaged:
            s.pwm.start( s.dc[0] )
        s.engaged = True

    def disengage( s ):
        if s.engaged:
            s.pwm.stop()
        s.engaged = False

    def move( s, speed ):
        s.engage()
        if speed:
            scale = s.dc[ 1 if speed > 0.0 else -1 ] - s.dc[0]
        else:
            scale = 0
        s.pwm.ChangeDutyCycle( s.dc[0] + scale*min( 1.0, abs(speed) ) )

    def stop( s, coast=False ):
        if coast:
            s.move(0)
        else:
            s.disengage()

    def goto( s, pos ):
        pass

class Environment():

    def __init__( s, dhtfile="DHT11" ):
        s.dhtfile = dhtfile

    def read( s ):
        readings = {}
        with open( s.dhtfile ) as f:
            dht = f.read().split()
        readings['humidity'] = float(dht[0])
        readings['temperature'] = float(dht[1])

        return readings

if __name__ == "__main__":
    from time import sleep
    try:
        c = Curtain()
        while True:
            sleep(0.1)
            print c.position()
    except KeyboardInterrupt:
        pass
    finally:
        cleanup()
