#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys, os, syslog, subprocess
import time
import atexit
import daemon
pidfile = "/run/sispmctl_turnoff.pid"

def error(message):
    syslog.syslog(syslog.LOG_ERR, message)
    sys.stderr.write("ALERT: "+message+"\n")
def debug(message):
    syslog.syslog(syslog.LOG_DEBUG, message)
    sys.stderr.write("DEBUG: "+message+"\n")

def delpidfile(pidfile):
    import os
    if os.path.exists(pidfile):
      os.remove(pidfile)
      print("PID file deleted")

def createpidfile(pidfile):
    pid = str(os.getpid())
    f = file(pidfile,"w+")
    f.write("%s\n" % pid)
    f.close()
    debug("PID file created")

with daemon.DaemonContext():
	try:
		atexit.register(syslog.closelog)
		syslog.openlog('sispmctl_turnoff', syslog.LOG_PID, syslog.LOG_LPR)
		if os.path.exists(pidfile):
				error("turnoff process already running -> exit")
				sys.exit(1)

		switchnr = sys.argv[1]
		if switchnr.isdigit() == False:
				error("first argument has to be a number")
				sys.exit(1)

		atexit.register(delpidfile,pidfile)
		createpidfile(pidfile)
		debug("PID file created")

		time.sleep(5*60) # wait for 5 minutes till switching off 

		debug("waiting time done, going to switch off outlet "+switchnr)
		command_off = ["/usr/bin/sispmctl","-f",nr]
		subprocess.check_call(command_off)
		debug("switched off outlet "+switchnr)
		sys.exit(0)
	except Exception as e:
		error("ERROR: "+str(e))


