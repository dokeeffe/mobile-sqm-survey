# mobile-sqm-survey

Collect light pollution data by driving around

## Requirements

- A Unihedron SQM-LU sky quality meter
- An android phone
- A laptop
- A Car

## Instructions

- Attach your SQM to the roof of your car pointing upwards
- Share your GPS from your phone using an app that can broadcast NMEA protocol
- Connect your laptop to the same WIFI as your phone (setup a hotspot)
- Plug in your SQM USB.
- Run the app specifying your phone's IP and USB device. Example `./survey.py  -i 192.168.43.1 -s /dev/ttyUSB0` Data will be printed to the console so you should probably redirect to a file by adding `> myfilename.csv`
- Drive around, data is logged every 5 seconds

Data contains timestamps in 2 formats, GPS coordinates and SQM readings

`2018-11-15 21:51:37,296 ,2018-11-15T21:51:35 , 53.503257667 , -8.45877888333 , 21.94`
