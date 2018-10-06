# Run refresh with a 20s sleep to avoid polling EC2 API too fast and breaking things
import subprocess
import time

while True:
    subprocess.check_call(['python', 'refresh.py'])
    time.sleep(20)
