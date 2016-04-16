if __name__ == "__main__":
    try:
        from os import uname, system
        from urllib2 import urlopen
        timesrc='http://www.timeapi.org/+8/now/'
        tm = urlopen( timesrc ).read()
        system( 'date -s %s' % tm )
    except ImportError:
        pass
