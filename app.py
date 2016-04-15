import time
from hardware import Curtain, LDR, cleanup

from datetime import datetime
import firebase

url = 'https://melatoninese.firebaseio.com/'
token = 'X0K8MoP5F55Q6S4lVKnf51piKE5HDttfAT1SlCpW'

fireBase = firebase.FirebaseApplication(url,token)


def main():
    print "Running"
    
    #check time
    currentTime = str(datetime.now().time).split(':')
    if currentTime[0] == '08':
        # if LDR > threshold1:
            # call the function to roll up the blind
        #else:
            # on the light switch
        
    elif currentTime[0] == '22':
        # call the function to roll down the blind
        
    else: 
        userControl = fireBase.get('/1D')
        if userControl['control']['manual'] == 'ON':

            # user curtain perefence
            if userControl['control']['curtain position'] == 0:
                #roll up the curtain
            else:
                # roll down the curtain

            # user table lamp pereference
            if userControl['control']['table lamp'] == 0:
                # off the table light
            else:
                # on the table light

            
        #else:
            # auto regulation suite
            
            # if LDR > threshold2 && LDR < threshold3:
                # roll the curtain down halfway
            # elif LDR > threshold3:
                # roll the curtain down fully
            # else:
                # roll the curtain back up
            
    
    

    



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
