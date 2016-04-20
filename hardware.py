from time import sleep
import RPi.GPIO as GPIO
GPIO.setmode( GPIO.BCM )

def cleanup():
    GPIO.cleanup()

class Curtain():

    def __init__( s, servo=18, encoder=(14,15) ):
        s.initservo( servo )
        s.initencoder( encoder )
        s.setdir()

    def setdir( s, closedir=1 ):
        s.closedir = closedir
        s.target = None

    def initservo( s, pin ):
        s.setservo()
        GPIO.setup( pin, GPIO.OUT )
        s.pwm = GPIO.PWM( pin, s.duty )

    def setservo( s, duty=50, mid=7.9, high=9.0, low=6.5 ):
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
        if speed:
            scale = s.dc[ 1 if speed > 0.0 else -1 ] - s.dc[0]
        else:
            scale = 0
        s.pwm.ChangeDutyCycle( s.dc[0] + scale*min( 1.0, abs(speed) ) )

    def update( s ):
        if s.target is None:
            return
        diff = s.target - s.position()
        if abs( diff ) < 0.1:
            s.move(0)
            s.target = None
        else:
            s.move( cmp( diff, 0 ) )

    def goto( s, pos ):
        s.target = s.closedir*max( 0.0, min( 1.0, pos ) )

class Light():

    def __init__( s, servo=23 ):
        s.initservo( servo )

    def initservo( s, pin ):
        s.setservo()
        GPIO.setup( pin, GPIO.OUT )
        s.pwm = GPIO.PWM( pin, s.duty )
        s.pwm.start( s.dc[0] )

    def setservo( s, duty=50, mid=7.3, high=5.7, low=8.5 ):
        s.duty = duty
        s.dc = ( mid, high, low )

    def move( s, m ):
        s.pwm.ChangeDutyCycle( s.dc[m] )

class Environment():

    def __init__( s, ldrpin=27, ldrscale=6000.0, dhtfile="DHT11" ):
        s.ldrpin = ldrpin
        s.ldrscale = ldrscale
        s.dhtfile = dhtfile

    def dht11( s ):
        with open( s.dhtfile ) as f:
            dht = f.read().split()
        # temperature, humidity
        return float(dht[1]), float(dht[0])

    def ldr( s, raw=False ):
        GPIO.setup( s.ldrpin, GPIO.OUT )
        GPIO.output( s.ldrpin, GPIO.LOW )
        sleep(0.1)
        GPIO.setup( s.ldrpin, GPIO.IN )
        reading = 0
        while reading < s.ldrscale and GPIO.input( s.ldrpin ) == GPIO.LOW:
            reading += 1
        if raw:
            return reading
        else:
            return max( 0.0, (s.ldrscale-reading)/s.ldrscale )

    def update( s ):
        s.temperature, s.humidity = s.dht11()
        s.light = s.ldr()

    def __repr__( s ):
        return "l: %.2f, t: %.2f, h: %.2f" % ( s.light, s.temperature, s.humidity )

if __name__ == "__main__":
    try:
        c = Curtain()
        l = Light()
        e = Environment()
        while True:
            sleep(0.1)
            # print c.position()
            e.update()
    except KeyboardInterrupt:
        pass
    finally:
        cleanup()
