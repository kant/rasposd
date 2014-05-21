import csv
import time
import datetime


class Fix:
    def __init__(self, data):
        if not isinstance(data[0], int) and data[0] != 'nan':
            data[0] = time.mktime(datetime.datetime.strptime(data[0], "%Y-%m-%dT%H:%M:%S.000Z").timetuple())

        self.time = data[0]
        self.ept = data[7]
        self.latitude = data[1]
        self.longitude = data[2]
        self.altitude = data[3]
        self.epx = data[5]
        self.epy = 0
        self.epv = data[6]
        #self.track = data[10]
        self.track = 0  # track is false in used record
        self.speed = data[8]
        self.climb = data[9]
        self.epd = 0
        self.eps = data[4]
        self.epc = 0
        self.mode = data[11]


class GPSRecord:

    def __init__(self, path):
        csvfile = open(path, 'rb')
        self.gps_data = csv.reader(csvfile, delimiter='\t', quotechar='"', skipinitialspace=True)
        next(self.gps_data, None)  # get header

    def next(self):
        data = self.gps_data.next()
        self.fix = Fix(data)
        #print data
