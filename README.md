# mobile-sqm-survey

Collect light pollution data by driving around in your car

## Requirements

- A Unihedron SQM-LU sky quality meter
- An android phone
- A laptop
- A car

## Instructions

- Attach your SQM to the roof of your car pointing upwards
- Share your GPS from your phone using an app that can broadcast NMEA protocol
- Connect your laptop to the same WIFI as your phone (setup a hotspot)
- Plug in your SQM USB.
- Run the app specifying your phone's IP and USB device. Example `./survey.py  -i 192.168.43.1 -s /dev/ttyUSB0` Data will be printed to the console and saved to a file called sqm.csv on mouse click
- Drive around, data is logged every time the left mouse button is clicked.
- Dont click and drive at the same time. Find a helpful assistant to click when driving in open areas with no tree cover or traffic

Data contains timestamps in 2 formats, GPS coordinates, altitude and SQM readings

`2018-11-15 21:51:37,296 ,2018-11-15T21:51:35 , 53.503257667,  -8.45877888333, 126, 21.94`
