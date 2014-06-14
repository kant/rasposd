from gps import *
import time
import threading
import dateutil.parser as dateparser

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
        self.nb_sats = 0

    def set(self, fix, nb_sats):
        try:
            fix.time = float(fix.time)
        except ValueError:
            fix.time = calendar.timegm(dateparser.parse(fix.time).timetuple())

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
        self.nb_sats = nb_sats

    def equals(self, dataset):
        return self.time == dataset.time

    def is_valid(self):
        return self.time != 'nan' and \
            self.latitude != 'nan' and \
            self.longitude != 'nan' and \
            self.altitude != 'nan' and \
            self.speed != 'nan' and \
            self.climb != 'nan'


class GpsReader(threading.Thread):
    '''
    http://www.stuffaboutcode.com/2013/09/raspberry-pi-gps-setup-and-python.html
    '''
    def __init__(self, freq):
        threading.Thread.__init__(self)

        self.gpsd = gps(mode=WATCH_ENABLE)  # starting the stream of info

        self.running = False

        self.data_set = GpsDataset()
        self.new_data_set = GpsDataset()
        self.new = False

        self.period = 1/freq

    def run(self):
        self.running = True

        while self.running:
            self.gpsd.next()

            self.new_data_set.set(self.gpsd.fix, self.gpsd.satellites_used)

            if self.new_data_set.is_valid():
                self.data_set = self.new_data_set
                self.new = True
		# print("new gps data")

            # time.sleep(self.period)
            time.sleep(0.05)

    def stop(self):
        self.running = False

    def is_new_data(self):
        was_new = self.new
        self.new = False
        return was_new

    def get_data(self):
        return self.data_set
