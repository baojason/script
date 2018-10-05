#!/usr/bin/python
from os import fork, setsid, umask, dup2
from sys import stdin, stdout, stderr

if fork():
    print "fork()"
    exit(0)
umask(0)
setsid()
if fork():
    print "fork()2"
    exit(0)

stdout.flush()
stderr.flush()
si = file('/dev/null', 'r')
so = file('/dev/null', 'a+')
se = file('/dev/null', 'a+', 0)
dup2(si.fileno(), stdin.fileno())
dup2(so.fileno(), stdout.fileno())
dup2(se.fileno(), stderr.fileno())
while True:
    print "sleep(1)"
    time.sleep(1)
