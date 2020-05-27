# Archived 
Use https://github.com/tmalch/cupsPowerOn as a more general solution
# sispm cups backend
a cups backend for using Gembird Programmable Power Outlet strips to automatically switch on a printer when cups receives a print job for it
### Requires
sispmctl http://sispmctl.sourceforge.net/ >= 3.0 (for support of older version see branch sispmctl2.x) 
python-daemon https://pypi.python.org/pypi/python-daemon/  
debian packages for both exist  
GEMBIRD (m)SiS-PM Programmable Power Outlet Strip   

tested on Ubuntu 14.04.3 LTS
### Installation
copy file (sispm) into cups backend folder (/usr/lib/cups/backend) and restart cups
sispmctl is expected at '/usr/bin/sispmctl'
### Usage
first get the URI for your printer eg. usb://Brother/HL-2030%20series  
then add a new printer, select Network Printer SISPMCTL - *continue*  
as Connection URI set sispm://outlet_number/original_URI   
*outlet_number* is the number of the outlet at the Sis-PM strip to which the printer is connected    
*original_URI* is the URI of the printer your retrieved in the first step  
eg. sispmctl://3/usb://Brother/HL-2030%20series
