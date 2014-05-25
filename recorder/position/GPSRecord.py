import csv
import time
import datetime


class Fix:
    def __init__(self, data):

        try:
            data[0] = float(data[0])
        except ValueError:
            data[0] = time.mktime(datetime.datetime.strptime(data[0], "%Y-%m-%dT%H:%M:%S.000Z").timetuple())

        self.time = data[0]
        self.ept = float(data[7])
        self.latitude = float(data[1])
        self.longitude = float(data[2])
        self.altitude = float(data[3])
        self.epx = float(data[5])
        self.epy = 0
        self.epv = float(data[6])
        #self.track = float(data[10])
        self.track = 0  # track is false in used record
        self.speed = float(data[8])
        self.climb = float(data[9])
        self.epd = float(0)
        self.eps = float(data[4])
        self.epc = 0
        self.mode = float(data[11])


class GPSRecord:

    def __init__(self, path):
        csvfile = open(path, 'rb')
        self.gps_data = csv.reader(csvfile, delimiter='\t', quotechar='"')
        next(self.gps_data, None)  # skip header


    def next(self):
        next_fix = self.gps_data.next()

        try:
            next_fix[0] = float(next_fix[0])
            self.fix = Fix(next_fix)
        except ValueError:
            print("Skip")
