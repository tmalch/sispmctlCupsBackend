#!/usr/bin/python
# -*- coding: utf-8 -*-
# cups backend to switch on GEMBIRD SIS-PM outlet before printing and switch off after some time
# based on mailto beckend by Robert Sander <robert.sander@epigenomics.com>
# (C) 2015 Thomas Malcher
# Released under GPL
# NO WARRANTY AT ALL
#
import sys, os, syslog, subprocess
import time
import atexit
import daemon
pidfile = "/run/sispmctl_turnoff.pid"
sispmctl_binary = "/usr/bin/sispmctl"

def error(message):
    syslog.syslog(syslog.LOG_ERR, message)
def debug(message):
    syslog.syslog(syslog.LOG_DEBUG, message)


def delpidfile(pidfile):
    import os
    if os.path.exists(pidfile):
      os.remove(pidfile)
      print("PID file deleted")

def createpidfile(pidfile):
		pid = str(os.getpid())
		with open(pidfile,"w+") as f:
			f.write("%s\n" % pid)
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
		command_off = [sispmctl_binary,"-f",switchnr]
		subprocess.check_call(command_off)
		debug("switched off outlet "+switchnr)
		sys.exit(0)
	except Exception as e:
		error("ERROR: "+str(e))
		sys.exit(1)


