# sispmctl cups backend
a cups backend for using Gembird Programmable Power Outlet strips to automatically switch on a printer when cups receives a print job for it
### Requires
sispmctl http://sispmctl.sourceforge.net/  
python-daemon https://pypi.python.org/pypi/python-daemon/  
debian packages for both exist  
tested on Ubuntu 14.04.3 LTS

### Installation
copy both files (sispmctl, sispmctl_turnoff.py) into cups backend folder (/usr/lib/cups/backend) and restart cups

