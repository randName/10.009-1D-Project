import time
from remote import Remote
from hardware import Curtain, Light, Environment, cleanup

def run_interval( interval ):
    def interval_decorator( func ):
        last_run = [0.0]
        def func_wrapper( *args ):
            if time.time() - last_run[0] > interval:
                func( *args )
                last_run[0] = time.time()
        return func_wrapper
    return interval_decorator

if __name__ == "__main__":

    curtain = Curtain()
    light = Light()
    env = Environment()
    remote = Remote( 'firebase.txt' )

    curtain.setencoder( limits=(0,50) )

    curtain.engage()

    @run_interval( 10 )
    def remote_check():
        print "Getting data from remote... ",
        remote.update()
        print "Done"

    @run_interval( 5 )
    def env_check():
        print "Getting data from environment... ",
        env.update()
        print env
        print "Done"

    @run_interval( 10 )
    def presets( cmd ):
        print cmd
        if cmd == "Auto":
            if env.light > 0.8 or env.temperature > 30:
                curtain.goto( 0.9 )
            elif env.light < 0.4 and env.temperature < 30:
                curtain.goto( 0.1 )
        elif cmd == "Wake":
            curtain.goto( 0.1 )
            if env.light < 0.4:
                light.goto(1)
        elif cmd == "Sleep":
            curtain.goto( 0.9 )
            if env.light > 0.8:
                light.goto(0)

    print "J.A.R.V.I.S. Activated"
    try:
        lastcmd = "Auto"
        while True:
            env_check()
            remote_check()
            cmd = remote.getcommand()[0]
            if cmd is not None and cmd != lastcmd:
                try:
                    curtain.goto( float( cmd ) )
                except ValueError:
                    pass
                lastcmd = cmd
            presets( lastcmd )
            curtain.update()
    except KeyboardInterrupt:
        print "J.A.R.V.I.S. Deactivated"
    finally:
        cleanup()
