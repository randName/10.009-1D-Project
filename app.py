import time
from remote import Remote
from hardware import Curtain, Environment, cleanup

def run_interval( interval ):
    def interval_decorator( func ):
        last_run = [0.0]
        def func_wrapper():
            if time.time() - last_run[0] > interval:
                func()
                last_run[0] = time.time()
        return func_wrapper
    return interval_decorator

if __name__ == "__main__":
    print "J.A.R.V.I.S. Activated"

    curtain = Curtain()
    env = Environment()
    remote = Remote( 'firebase.txt' )

    try:
        while True:
            # remote_check()
            # env_check()
    except KeyboardInterrupt:
        print "J.A.R.V.I.S. Deactivated"
    finally:
        cleanup()
