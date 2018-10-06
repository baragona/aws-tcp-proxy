# This launches another command and passes all the arguments through
# Restarts it with a 5 second sleep if it ever dies...
import subprocess
import sys
import time

cmd_list = sys.argv[:1]
while True:
    try:
        print('Calling in keep_alive.py:')
        print(cmd_list)
        subprocess.check_call(cmd_list)
        print('keep_alive.py has caught a process exit(0) in cmd:')
        print(cmd_list)
    except subprocess.CalledProcessError:
        print('keep_alive.py has caught a process death in cmd:')
        print(cmd_list)
    time.sleep(5)
