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

    curtain = Curtain()
    env = Environment()
    remote = Remote( 'firebase.txt' )

    curtain.engage()

    @run_interval( 10 )
    def remote_check():
        print "Getting data from remote... ",
        remote.update()
        print "Done"

    @run_interval( 20 )
    def env_check():
        print "Getting data from environment... ",
        env.update()
        print "Done"

    def main():
        cmd = remote.getcommand()[0]

        if cmd is None or cmd == lastcmd:
            return

        try:
            curtain.goto( float( cmd ) )
            lastcmd = cmd
            return
        except ValueError:
            pass

        if cmd == "auto":
            if env.light > 0.8 or env.temperature > 30:
                curtain.goto( 0.9 )
            elif env.light < 0.4 and env.temperature < 30:
                curtain.goto( 0.1 )
        elif cmd == "wake":
            curtain.goto( 0.1 )
        elif cmd == "sleep":
            curtain.goto( 0.9 )

        lastcmd = cmd

    print "J.A.R.V.I.S. Activated"
    try:
        lastcmd = None
        while True:
            remote_check()
            env_check()
            main()
            curtain.update()
    except KeyboardInterrupt:
        print "J.A.R.V.I.S. Deactivated"
    finally:
        cleanup()
