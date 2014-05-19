from gps import *
import time
import threading
import csv


class GpsRecorder(threading.Thread):
    '''
    http://www.stuffaboutcode.com/2013/09/raspberry-pi-gps-setup-and-python.html
    '''
    def __init__(self, directory):
        threading.Thread.__init__(self)
        self.gpsd = gps(mode=WATCH_ENABLE) #starting the stream of info

        self.output = open(directory + 'data_gps.csv', "wb")
        self.writer = csv.writer(self.output, delimiter='\t', quotechar='"', quoting=csv.QUOTE_NONNUMERIC)
        self.running = False

    def run(self):
        self.running = True

        self.writer.writerow([
            "mesure_time",
            "latitude", "longitude",
            "altitude",
            "eps", "epx", "epv",  "ept",
            "speed", "climb",
            "track", "mode", "sats"
        ])

        while self.running:
            # grab EACH set of gpsd info to clear the buffer
            self.gpsd.next()

            self.writer.writerow([
                self.gpsd.fix.time,
                self.gpsd.fix.latitude, self.gpsd.fix.longitude,
                self.gpsd.fix.altitude,
                self.gpsd.fix.eps, self.gpsd.fix.epx, self.gpsd.fix.epv, self.gpsd.fix.ept,
                self.gpsd.fix.speed, self.gpsd.fix.climb,
                self.gpsd.fix.track, self.gpsd.fix.mode, self.gpsd.satellites
            ])
            time.sleep(0.5)

    def stop(self):
        self.running = False
