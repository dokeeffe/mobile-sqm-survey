#!/usr/bin/env python

from __future__ import print_function
import requests
import argparse
import time
import logging
import sys
import serial
import pynmea2
import socket
import threading
from datetime import datetime
from pymouse import PyMouseEvent

log = logging.getLogger()
logging.basicConfig(format='%(asctime)s ,%(message)s', level=logging.INFO, filename='sqm.csv')

class SetupException(Exception):
    pass

class SqmReader:
    def __init__(self, port):
        self.ser = serial.Serial(
            port=port,\
            baudrate=115200,\
            parity=serial.PARITY_NONE,\
            stopbits=serial.STOPBITS_ONE,\
            bytesize=serial.EIGHTBITS,\
            timeout=1)

    def read(self):
        self.ser.write("rx\n")
        self.ser.flush()
        raw = self.ser.readline()
        try:
            return raw.split(',')[1].replace('m','')
        except Exception:
            return ''

    def close(self):
        self.ser.close()

class TCPReader:
    def __init__(self, host, port):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            self.sock.connect((host, port))
        except socket.error as err:
            print("TCP setup: Could not bind to {}:{}. Error: {}".format(host, port, err))
            raise SetupException()

    def iter(self):
        while True:
            data, addr = self.sock.recvfrom(1024)
            if not data:
                break
            if data[-1] != "\n":
                data = data + "\n"
            yield data
        self.sock.close()

class GpsPoller(threading.Thread):
    def __init__(self, ip, port):
        threading.Thread.__init__(self)
        self.tcp_reader = TCPReader(ip,port)
        self.runnable = True
        self.latest = ''

    def run(self):
        lat = 0
        lon = 0
        altitude = 0
        gotUpdate = False

        reader = pynmea2.NMEAStreamReader()

        for data in self.tcp_reader.iter(): 
            if not self.runnable:
                return
            try:
                data = data.decode('UTF-8')
            except AttributeError:
                pass
            try:
                for msg in reader.next(data):
                    if type(msg) == pynmea2.types.talker.GGA:
                        lat = msg.latitude
                        lon = msg.longitude
                        altitude = msg.altitude
                        gotUpdate = True

            except pynmea2.ParseError as e:
                pass
                log.debug("Error while parsing NMEA string: {}".format(e))

            if gotUpdate:
                timestamp = datetime.now().replace(microsecond=0).isoformat()
                self.latest = '{}, {}, {}, {}'.format(timestamp, lat, lon, altitude)
                gotUpdate = False
            
    
class MouseClickRecorder(PyMouseEvent):
    def __init__(self, ip, port, sqm):
        PyMouseEvent.__init__(self)
        self.gps = GpsPoller(ip, port)
        self.sqm_reader = SqmReader(sqm)
        self.gps.start()

    def click(self, x, y, button, press):
        '''Print Fibonacci numbers when the left click is pressed.'''
        if button == 1:
            if press:
                captured = False
                while not captured:
                    if self.gps.latest is not '':
                        sqm = self.sqm_reader.read()
                        print('{},   {}'.format(self.gps.latest, sqm))
                        log.info('{}, {}'.format(self.gps.latest, sqm))
                        self.gps.latest = ''
                        captured = True
                    time.sleep(1) 

    def stop(self):
        self.sqm_reader.close()
        self.gps.runnable = False
        self.gps.join()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('-p', '--port', help="Port to listen for TCP packets", type=int, default=10110)
    parser.add_argument('-i', '--ip', help="Host to listen for GPS data. Share GPS from your smartphone and enter the address here", type=str, default='')
    parser.add_argument('-s', '--sqm', help="SQM device path, default /dev/ttyUSB0", type=str, default='/dev/ttyUSB0')
    args = parser.parse_args()

    if not (args.ip):
        parser.print_help()
        print("ERROR: Please specify TCP port to use")
        sys.exit(1)

    if args.ip:
        c = MouseClickRecorder(args.ip, args.port, args.sqm)
        c.run()
       
if __name__ == "__main__":
    main()
