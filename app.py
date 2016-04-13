import time
from hardware import Curtain, LDR, cleanup

from datetime import datetime
import firebase

url = 'https://melatoninese.firebaseio.com/'
token = 'X0K8MoP5F55Q6S4lVKnf51piKE5HDttfAT1SlCpW'

def main():
    print "Running"
    #check time
    currentTime = str(datetime.now().time).split(':')
    if currentTime[0] == '08':
        # call the function to roll up the blind
        
    elif currentTime[0] == '22':
        # call the function to roll down the blind
        
    else: # check for input in firebase
    
    

    



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
