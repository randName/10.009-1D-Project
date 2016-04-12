import RPi.GPIO as GPIO

class Curtain():

    def __init__( s, pin=18, duty=100, mid=50, high=100, low=0 ):
        s.pin = pin
        s.duty = duty
        s.dc = ( mid, high, low )

        GPIO.setmode( GPIO.BCM )
        GPIO.setup( s.pin, GPIO.OUT )
        s.pwm = GPIO.PWM( s.pin, s.duty )

    def move( s, speed ):
        s.pwm.start( s.mid )
        if speed:
            z = 1 if speed > 0.0 else -1
            speed = z*min( 1.0, abs(speed) )*( s.dc[z] - s.dc[0] )
            s.pwm.ChangeDutyCycle( s.dc[0] + speed )

    def stop( s ):
        s.move(0)

    def disengage( s ):
        s.pwm.stop()

    def position( s ):
        pass

if __name__ == "__main__":
    c = Curtain()
