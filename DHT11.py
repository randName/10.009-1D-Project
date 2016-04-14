import Adafruit_DHT
from time import sleep

pin = '5'
logfile = 'DHT11'

try:
    while True:
        data = Adafruit_DHT.read_retry( Adafruit_DHT.DHT11, pin )
        print "hum: %s\t temp: %s" % data
        with open( logfile, 'w' ) as f:
            f.write( "%s\n%s" % data )
        sleep(1)
except KeyboardInterrupt:
    print "Exiting"
