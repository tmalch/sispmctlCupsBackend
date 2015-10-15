#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys, os, syslog, subprocess
import time
import atexit
import signal

pidfile = "/run/sispmctl_turnoff.pid"

def writelog(message):
    syslog.syslog(syslog.LOG_ALERT, message)
    sys.stderr.write(message)

def switchoff(nr):
    command_off = ["/usr/bin/sispmctl","-f",nr]
    try:
      subprocess.check_call(command_off)
    except:
      writelog("ERROR konnte NR %s nicht ausschalten" % nr)

def delpidfile(pidfile):
    import os
    if os.path.exists(pidfile):
      os.remove(pidfile)
      print("INFO PID file gelöscht\n")

def createpidfile(pidfile):
    pid = str(os.getpid())
    f = file(pidfile,"w+")
    f.write("%s\n" % pid)
    f.close()
    writelog("INFO PID file erstellt\n")


import daemon
with daemon.DaemonContext():
	atexit.register(syslog.closelog)
	syslog.openlog('sispmctl_printer', syslog.LOG_PID, syslog.LOG_LPR)
	try:
		switchnr = sys.argv[1]
		if switchnr.isdigit() == False:
				writelog("ERROR 1. Argument ist keine Nummer")
				sys.exit(1)

		if os.path.exists(pidfile):
				writelog("ERROR turnoff läuft bereits")
				sys.exit(1)

		atexit.register(delpidfile,pidfile)
		createpidfile(pidfile)
		writelog("INFO PID file created")

		time.sleep(5*60) # wait for 5 minutes till switching off 

		writelog("INFO: Wartezeit vorbei switch off")
		switchoff(switchnr)
		writelog("INFO: switched off FERTIG")

		sys.exit(0)
	except Exception as e:
		writelog("ERROR: "+str(e))


