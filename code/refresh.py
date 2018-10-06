import os.path
import signal
import subprocess
import traceback
from os import listdir
from os.path import isfile, join

import boto3
import requests

r = requests.get("http://169.254.169.254/latest/dynamic/instance-identity/document")
response_json = r.json()
region = response_json.get('region')
instance_id = response_json.get('instanceId')

ec2 = boto3.resource('ec2', region_name=region)
instance = ec2.Instance(instance_id)
tags = instance.tags or []

# something like [{u'Value': 'myserverlesscluster.cluster-abcdefgh.us-west-2.rds.amazonaws.com:3306', u'Key': '7777'}]

print tags

ports_to_keep = set()
for tag in tags:
    try:
        key = tag['Key']
        ports_to_keep.add(key) # do this early in the try catch
        value = tag['Value']
        if not key.isdigit():
            print('key is not a port number, skipping:' + key)
            continue
        targetfile = 'listeners/%s' % (key)
        pidfile = 'pidfiles/%s' % (key)
        if os.path.isfile(targetfile) and open(targetfile, 'rb').read() == value:
            print('listener already exists for ' + key)
            continue
        if os.path.isfile(targetfile) and open(targetfile, 'rb').read() != value:
            print('listener already exists but has the wrong target ' + key)
            tokill = int(open(pidfile, 'rb').read())
            os.killpg(os.getpgid(tokill), signal.SIGKILL)
        print('creating new listener...')
        process = subprocess.Popen(['python', 'keep_alive.py', 'socat', 'TCP-LISTEN:' + key + ',fork', 'TCP:' + value],
                                   close_fds=True, preexec_fn=os.setsid)
        pid = process.pid
        print('created socat pid:' + str(pid))
        open(targetfile, 'wb').write(value)
        open(pidfile, 'wb').write(str(pid))
    except Exception: # I know what you're thinking and you're wrong
        print('Caught error looping over instance tags:')
        traceback.print_exc()


# now kill any listeners that should go away b/c the tag went byebye
existing_listener_ports = [f for f in listdir('listeners/') if isfile(join('listeners/', f))]
for existing_port in existing_listener_ports:
    if existing_port not in ports_to_keep:
        try:
            print('listener should go bye-bye:' + existing_port)
            targetfile = 'listeners/%s' % (existing_port)
            pidfile = 'pidfiles/%s' % (existing_port)
            tokill = int(open(pidfile, 'rb').read())
            os.killpg(os.getpgid(tokill), signal.SIGKILL)
            os.remove(pidfile)
            os.remove(targetfile)
            print('fully removed listener:' + existing_port)
        except Exception: # I know what you're thinking and you're wrong
            print('Caught error looping over existing listner ports:')
            traceback.print_exc()
