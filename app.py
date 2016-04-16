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

    @run_interval( 10 )
    def remote_check():
        print "Getting data from remote... ",
        remote.fetch()
        print "Done"

    @run_interval( 30 )
    def env_check():
        print "Getting data from environment... ",
        env.update()
        print "Done"

    def main():
        cmd = remote.getcommand()

        if cmd[0] is not None:
            curtain.goto( cmd[0] )

        # env.light
        # env.temperature

    print "J.A.R.V.I.S. Activated"
    try:
        while True:
            remote_check()
            env_check()
            main()
            curtain.update()
    except KeyboardInterrupt:
        print "J.A.R.V.I.S. Deactivated"
    finally:
        cleanup()
