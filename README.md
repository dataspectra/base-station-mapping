# imsi_for_fun
Just a bunch of scripts to have fun with IMSIs

# Dependencies

1. Download and install redis in the parent directory, launch redis with the script in the `cache` directory.
2. Install the dependencies with pipenv
3. For IMSI catching: https://github.com/Oros42/IMSI-catcher

# Usage

1. Fetch a cell datacet from Mozilla: https://location.services.mozilla.com/downloads
2. Unpack it
3. Launch `0_mls_loader.py`
4. Plug the antenna
5. Run `1_lookup_scan.py`

A directory with the current date is created and contain the output of the script.


* `found.txt`: The cell is known in the database, get the location of it, generate a link for OSM 
* `notfound.txt`: The cell isn't know in the database
* `dafuck.txt`: The MCC is not known in the database (often 0, probably an error during the scan)

# grgsm-burst

This script intends to be used on low computing power devices (Rpi 3/4, OrangePi). The script stores bursts in a file specified with -b, -s is the sampling rate--900001 being the lowest:
```bash
$./grgsm_burst -f 940.4e6 -s900001 --args=rtl=0 -b myfile.burst
```
Try different value for s until you get decent output.

To extract IMSI numbers from this burst file, one would use grgsm_decode and the `simpleIMSIcatcher.py` script as the following:
```bash
$grgsm_decode -b myfile.burst -v
#simple_IMSI-catcher.py --sniff
```
