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
import signal
import atexit

def writelog(message):
    #syslog.syslog(syslog.LOG_ALERT, message)
    sys.stderr.write(message)

def switchon(nr):
    command_on = ["/usr/bin/sispmctl","-o",str(nr)]
    subprocess.check_call(command_on)
    writelog("INFO NR "+str(nr)+" einschaltet")

def turnOFFproc(nr):
    subprocess.Popen(['/usr/lib/cups/backend/sispmctl_turnoff.py',str(nr)])

argc = len(sys.argv)
pidfile = "/run/sispmctl_turnoff.pid"
atexit.register(syslog.closelog)
syslog.openlog('sispmctl_printer', syslog.LOG_PID, syslog.LOG_LPR)

writelog("INFO: switchprinter argv[%s] = '%s'\n" % (argc, "', '".join(sys.argv)))

if argc == 1:
    print "direct sispmctl \"Unknown\" \"SISPMCTL\""
    sys.exit(0)

if argc < 6 or argc > 7:
    writelog("ERROR: %s job-id user title copies options [file]\n" % sys.argv[0])
    sys.exit(1)

jobid = sys.argv[1]
user = sys.argv[2]
title = sys.argv[3]
copies = sys.argv[4]
if title[:7] == "smbprn.":
    title = title[16:]
opts = sys.argv[5].split(" ")
deviceuri = os.environ['DEVICE_URI']
#deviceuri = "sispmctl://4/usb://Brother/HL-2030%20series"
try:
	if argc == 7:
		  writelog("INFO: file is %s\n" % sys.argv[6])
		  infilename = sys.argv[6]
	else:
		  infilename = os.environ['TMPDIR']+"/"+user+jobid+".tmp"
		  try:
		      infile = open(infilename, "w")
		  except:
		      writelog("ERROR: unable to create tmp file %s\n" % infilename)
		      sys.exit(1)
		  writelog("INFO: file is stdin\n")
		  try:
		      infile.write(sys.stdin.read())
		  except:
		      writelog("ERROR: unable to copy into tmpfile\n")
		      sys.exit(1)
		  infile.close()
		  writelog("INFO: copied stdin to %s\n" % infilename)

	writelog("INFO: Deviceuri %s\n" % deviceuri)
	##Parameter auslesen entweder aus URI oder Option (URI hat Vorang)
	switchnr = None
	if deviceuri[:11] == "sispmctl://":
		  nested_uri_idx = deviceuri.find("/", 11)
		  if nested_uri_idx < 0:
		    writelog("ERROR: falsche URI %s\n" % deviceuri)
		    sys.exit(2)
		  switchnr = str(int(deviceuri[11:nested_uri_idx]))
		  deviceuri = deviceuri[nested_uri_idx+1:]
		  writelog("INFO: deviceuri %s\n" % deviceuri)
	else:
		  writelog("INFO: suche in options\n")
		  for opt in opts:
		    if opt[:9] == "switchnr=":
			  	switchnr = str(int(opt[9:]))
			  	writelog("INFO: SwitchNr %d\n" % switchnr)

	if os.path.exists(pidfile):
	    writelog("INFO TURNOFF Exists --> stop\n")
	    try:
	      tpid = open(pidfile,"r").readline(10)
	      os.kill(int(tpid), signal.SIGTERM)
	    except Exception as e:
	      os.remove(pidfile)
	      writelog("ERROR konnte turnoff nicht beenden"+str(e))
	#if it is off:
	switchon(switchnr)
	time.sleep(10)


	i = deviceuri.find(":")
	backend = "/usr/lib/cups/backend/"+deviceuri[:i]
	writelog("ERROR: backend %s\n" % backend)
	os.environ['DEVICE_URI'] = deviceuri

	title = "\""+title+"\""
	options = "\""+" ".join(opts[0:])+"\""
	command = [backend,jobid,user,title,copies,options,infilename]
	writelog("INFO Exec backend %s\n" % " ".join(command[0:]))

	p = subprocess.Popen(command,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
	p.wait()
	
	writelog("INFO: usb backend ist fertig.\n")
	turnOFFproc(switchnr)
	writelog("INFO: turnoff started.\n")

except Exception as e:
	writelog(str(e)+"\n")

sys.exit(0)



