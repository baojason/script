#!/usr/bin/python
import os
import time
import sys
import subprocess
from os import dup2
from sys import stdin, stdout, stderr

mainPid = os.getpid()
print("Main Pid: %s" % mainPid)
installScript = sys.argv[1]

pid = os.fork()

if pid > 0:
    print("Run the dml installation at the background!!!")
    print("New pid: %u" % pid)
    time.sleep(1)
    print("Main process quit")
    sys.exit(0)

#os.setsid()
'''
for x in range(1, 1000):
    print("spid: %s, ppid: %s pgid: %s" % (os.getpid(), os.getppid(), os.getpgid(0)))
    time.sleep(1)
'''
stdout.flush()
stderr.flush()
si = file('/dev/null', 'r')
#so = file('/dev/null', 'a+')
so = file('/var/log/instdml.log', 'a+')
se = file('/dev/null', 'a+', 0)
dup2(si.fileno(), stdin.fileno())
dup2(so.fileno(), stdout.fileno())
dup2(se.fileno(), stderr.fileno())

print "start"
subprocess.check_call(['./.dmlinstart', installScript])
print "end"
