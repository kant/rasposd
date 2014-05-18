from gps import *
import smbus
import csv
import threading
import math

from position.bitify.python.sensors.gy88 import GY88
from position.bitify.python.utils.i2cutils import i2c_raspberry_pi_bus_number

gyro_address = 0x68
compass_address = 0x1e
barometer_address = 0x77


class ImuDataset():

    def __init__(self):
        self.time = 0
        self.pitch = 0
        self.roll = 0
        self.yaw = 0
        self.gyro_scaled_x = 0
        self.gyro_scaled_y = 0
        self.gyro_scaled_z = 0
        self.accel_scaled_x = 0
        self.accel_scaled_y = 0
        self.accel_scaled_z = 0
        self.temperature = 0
        self.pressure = 0

    def set(self, data):
        self.time = data[0]
        self.pitch = data[1]
        self.roll = data[2]
        self.yaw = data[3]
        self.gyro_scaled_x = data[4]
        self.gyro_scaled_y = data[5]
        self.gyro_scaled_z = data[6]
        self.accel_scaled_x = data[7]
        self.accel_scaled_y = data[8]
        self.accel_scaled_z = data[9]
        self.temperature = data[10]
        self.pressure = data[11]

    def equals(self, dataset):
        return self.pitch == dataset.pitch and \
            self.roll == dataset.roll and \
            self.yaw == dataset.yaw and \
            self.accel_scaled_x == dataset.accel_scaled_x and \
            self.accel_scaled_y == dataset.accel_scaled_y and \
            self.accel_scaled_z == dataset.accel_scaled_z and \
            self.temperature == dataset.temperature and \
            self.pressure == dataset.pressure


class GpsDataset():

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

    def equals(self, dataset):
        return self.time == dataset.time


class PositionRecorder(threading.Thread):

    def __init__(self, directory):
        threading.Thread.__init__(self)
        self.bus = smbus.SMBus(i2c_raspberry_pi_bus_number())
        self.imu = GY88(self.bus, gyro_address, compass_address, barometer_address, "GY88")
        self.gpsd = gps(mode=WATCH_ENABLE) #starting the stream of info
        #self.output = open(directory + 'data_pos.csv', "wb")
        self.output = open('/dev/stdout', "wb")
        self.writer = csv.writer(self.output, delimiter='\t', quotechar='"', quoting=csv.QUOTE_NONNUMERIC)
        self.running = False

        self.imu_data = NaN
        self.imu_data_old = NaN
        self.gps_data = NaN
        self.gps_data_old = NaN

        self.imu_changed = False
        self.gps_changed = False

        self.time = 0
        self.gps_time = 0
        self.imu_time = 0

        self.speed = 0
        self.climb = 0

        self.latitude = 0
        self.longitude = 0

        self.altitude = 0
        self.pressure_ref = 0

        self.temperature = 0

        self.track = 0
        self.mode = 0
        self.sats = NaN

        self.pitch = 0
        self.roll = 0
        self.yaw = 0

    def run(self):
        self.running = True

        self.writer.writerow([
            "time",
            "pitch", "roll", "yaw",
            "speed", "climb",
            "latitude", "longitude",
            "altitude", "temperature"
            "track", "mode", "sats"
        ])

        self.imu_data = ImuDataset()
        self.gps_data = GpsDataset()

        while self.running:
            # Read data from sensors

            # Save old data
            self.imu_data_old = self.imu_data
            self.gps_data_old = self.gps_data

            # Get new data
            self.imu_data.set(self.imu.read_all())
            self.gpsd.read()
            self.gps_data.set(self.gpsd.fix)

            self.imu_changed = not self.imu_data.equals(self.imu_data_old)
            self.gps_changed = not self.gps_data.equals(self.gps_data_old)

            # Compute final data

            if self.gps_changed:
                self.time = self.gps_data.time
                self.gps_time = self.time

                self.speed = self.gps_data.speed
                self.climb = self.gps_data.climb

                self.latitude = self.gps_data.latitude
                self.longitude = self.gps_data.longitude

                self.altitude = self.gps_data.altitude
                self.pressure_ref = self.imu_data.pressure

                self.temperature = self.gps_data.temperature

                self.track = self.gps_data.track
                self.mode = self.gps_data.mode
                self.sats = self.gps_data.sats
            else:
                if self.imu_changed:

                    self.imu_time.delta = self.imu_data.time - self.imu_time
                    self.imu_time = self.imu_data.time

                    self.time += self.imu_time.delta

                    self.speed += self.imu_data.accel_scaled_x*self.imu_time.delta
                    self.climb += self.imu_data.accel_scaled_z*self.imu_time.delta

                    self.altitude = self.gps_data.altitude + (self.imu_data.pressure-self.pressure_ref)*8

            if self.imu_changed:

                self.pitch = self.imu_data.pitch
                self.roll = self.imu_data.roll
                self.yaw = self.imu_data.yaw

                self.temperature = self.imu_data.temperature

            # Write data line to CSV file
            self.writer.writerow([
                self.time,
                self.pitch, self.roll, self.yaw,
                self.speed, self.climb,
                self.latitude, self.longitude,
                self.altitude, self.temperature,
                self.track, self.mode, self.sats
            ])

    def stop(self):
        self.running = False
