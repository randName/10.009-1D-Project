from datetime import datetime, time
from firebase import FirebaseApplication

class Remote():

    def __init__( s, cred=None, basenode='/1d/control/' ):
        if isinstance( cred, basestring ):
            with open( cred ) as f:
                cred = f.read().split()
        s.conn = FirebaseApplication( *cred )
        s.basenode = basenode

    def fetch( s ):
        rem = s.conn.get( s.basenode )
        s.data = zip( rem['manual'], rem['scheduler'] )
        s.alarm = rem.get('alarm')

    def activate( s, tm, threshold=300 ):
        td = tm - s.now
        return td.days == 0 and td.seconds <= threshold

    def getcommand( s ):
        s.now = datetime.now()

        def getval( object ):
            if object[0][0]:
                if s.activate( datetime.fromtimestamp( object[0][0] ) ):
                    return object[0][1]
            for t in sorted( object[1].keys() ):
                tm = datetime.strptime( t, '%H:%M' )
                if s.activate( datetime.combine( s.now, time(tm.hour,tm.minute) ) ):
                    return object[1][t]

        return [ getval( object ) for object in s.data ]

if __name__ == "__main__":
    r = Remote( 'firebase.txt' )
    r.fetch()
    print r.getcommand()
