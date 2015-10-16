# sispm cups backend
a cups backend for using Gembird Programmable Power Outlet strips to automatically switch on a printer when cups receives a print job for it
### Requires
sispmctl http://sispmctl.sourceforge.net/  
python-daemon https://pypi.python.org/pypi/python-daemon/  
debian packages for both exist  
tested on Ubuntu 14.04.3 LTS

### Installation
copy both files (sispm, sispm_turnoff) into cups backend folder (/usr/lib/cups/backend) and restart cups
sispmctl is expected at '/usr/bin/sispmctl'
### Usage
first get the URI for your printer eg. usb://Brother/HL-2030%20series  
then add a new printer, select Network Printer SISPM auto power on - *continue*  
as Connection URI set sispm://outlet_number/original_URI where    
*outlet_number* is the number of the outlet at the Sis-PM strip to which the printer is connected    
*original_URI* is the URI of the printer you retrieved in the first step  
eg. sispmctl://3/usb://Brother/HL-2030%20series
