from gps import *
import time
import threading


class GpsDataset:

    def __init__(self):
        self.time = 0
        self.ept = 0
        self.latitude = 0
        self.longitude = 0
        self.altitude = 0
        self.epx = 0
        self.epy = 0
        self.epv = 0
        self.track = 0
        self.speed = 0
        self.climb = 0
        self.epd = 0
        self.eps = 0
        self.epc = 0
        self.mode = 0
        #self.sats = NaN

    def set(self, fix):
        self.time = fix.time
        self.ept = fix.ept
        self.latitude = fix.latitude
        self.longitude = fix.longitude
        self.altitude = fix.altitude
        self.epx = fix.epx
        self.epy = fix.epy
        self.epv = fix.epv
        self.track = fix.track
        self.speed = fix.speed
        self.climb = fix.climb
        self.epd = fix.epd
        self.eps = fix.eps
        self.epc = fix.epc
        self.mode = fix.mode
        #self.sats = fix.sats

    def equals(self, dataset):
        return self.time == dataset.time


class GpsRecorder(threading.Thread):
    '''
    http://www.stuffaboutcode.com/2013/09/raspberry-pi-gps-setup-and-python.html
    '''
    def __init__(self):
        threading.Thread.__init__(self)
        self.gpsd = gps(mode=WATCH_ENABLE) #starting the stream of info

        self.running = False

        self.data_set = GpsDataset()
        self.new = False

    def run(self):
        self.running = True

        while self.running:
            self.gpsd.next()

            self.data_set.set(self.gpsd.fix)
            self.new = True

            time.sleep(0.9)

    def stop(self):
        self.running = False

    def is_new_data(self):
        was_new = self.new
        self.new = False
        return was_new

    def get_data(self):
        return self.data_set