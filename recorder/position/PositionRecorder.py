from gps import *
import smbus
import csv
import threading

import GPSReader as GPSReader
import IMUReader as IMUReader


class PositionRecorder(threading.Thread):

    def __init__(self, directory):
        threading.Thread.__init__(self)
        self.imu = IMUReader.ImuRecorder()
        self.gps = GPSReader.GpsRecorder()

        self.imu.start()
        self.gps.start()

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
            "lat", "lon",
            "alt", "temp",
            "track", "mode", "sats"
        ])

        self.imu_data = self.imu.get_data()
        self.gps_data = self.gps.get_data()

        while self.running:
            # Read data from sensors

            imu_new = self.imu.is_new_data()
            gps_new = self.gps.is_new_data()

            if imu_new:
                print("New IMU data")
                self.imu_data_old = self.imu_data
                self.imu_data = self.imu.get_data()

            if gps_new:
                print("New GPS data")
                self.gps_data_old = self.gps_data
                self.gps_data = self.gps.get_data()

            if not imu_new and not gps_new:
                continue

            # Compute final data
            if gps_new:

                self.gps_data = self.gps.get_data()

                self.time = self.gps_data.time
                self.gps_time = self.time

                self.speed = self.gps_data.speed
                self.climb = self.gps_data.climb

                self.latitude = self.gps_data.latitude
                self.longitude = self.gps_data.longitude

                self.altitude = self.gps_data.altitude
                self.pressure_ref = self.imu_data.pressure

                self.track = self.gps_data.track
                self.mode = self.gps_data.mode
                #self.sats = self.gps_data.sats
            else:
                print("No GPS data")
                if imu_new:

                    imu_time_delta = self.imu_data.time - self.imu_time
                    self.imu_time = imu_time_delta

                    self.time += imu_time_delta

                    self.speed += self.imu_data.accel_scaled_x*imu_time_delta
                    self.climb += self.imu_data.accel_scaled_z*imu_time_delta

                    self.altitude = self.gps_data.altitude + (self.imu_data.pressure-self.pressure_ref)*8

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
            self.output.flush()

    def stop(self):
        self.running = False

        self.imu.stop()
        self.gps.stop()
