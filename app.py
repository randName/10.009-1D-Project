import time

from hardware import Curtain, LDR, cleanup

def main():
    print "Running"
    # check time

    # check light

    # check firebase

if __name__ == "__main__":
    print "J.A.R.V.I.S. Activated"
    
    refresh_interval = 5
    last_time = 0

    try:
        while True:
            if time.time() - last_time > refresh_interval:
                main()
                last_time = time.time()
    except KeyboardInterrupt:
        print "J.A.R.V.I.S. Deactivated"
    finally:
        cleanup()
