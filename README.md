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
- Run the app specifying your phone's IP and USB device. Example `./survey.py  -i 192.168.43.1 -s /dev/ttyUSB0`
