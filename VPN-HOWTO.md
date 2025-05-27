# VPN-HOWTO

Phoebus defaults to using EPICS PV-access. Currently, we're unable to access this over a VPN.
The solution is to switch to using EPICS Channel Access (CA) and additionally to pass name-hint information
as environment variables to Phoebus on Launch

## Create a set of ip-addresses to search

Assuming a hosts(5) file of ip-address->DNS name mappings, save as follows

cat HOSTS-SUBSET | ./hosts2ioc_addr.conf > hosts2ioc_addr.conf

## Set default ca

echo "org.phoebus.pv/default=ca" > src/settings_base.ini

## Create workspace in the normal way - hosts2ioc_addr.conf forces use of environment variables to set CA values

./run_phoebus.sh UUT


## Bonus run a multiple workspace remotely

example - creates WS multi_acq1102_043_acq1102_044_acq1102_045_acq1102_046
```
./ACQ400CSSP_launcher.py acq1102_043 acq1102_044 acq1102_045 acq1102_046
# close Phoebus and run
./run_phoebus.sh multi_acq1102_043_acq1102_044_acq1102_045_acq1102_046
```


