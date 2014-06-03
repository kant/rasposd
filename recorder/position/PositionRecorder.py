from gps import *
import csv
import threading
import datetime
import ConfigParser
import os
from time import sleep

import GPSReader as GPSReader
import IMUReader as IMUReader

RAD_TO_DEG = 57.2957795131 # 180/math.pi
MPS_TO_KPH = 3.6

class PositionRecorder(threading.Thread):

    def __init__(self, single_record_dir, magnetometer_calibration):
        threading.Thread.__init__(self)

        self.set_config('config/position.cfg')

        self.imu = IMUReader.ImuReader(magnetometer_calibration, self.sim, self.path + 'feed/data_imu.csv')
        self.gps = GPSReader.GpsReader(self.sim, self.path + 'feed/data_gps.csv')

        self.imu.start()
        self.gps.start()

        if self.to_stdout:
            self.output = open('/dev/stdout', "wb")
        else:
            self.output = open(self.path + single_record_dir + self.filename, "wb")

        self.writer = csv.writer(self.output, delimiter='\t', quotechar='"', quoting=csv.QUOTE_NONNUMERIC)
        self.running = False

        self.gps_fixed = False

        self.imu_data = NaN
        self.imu_data_old = NaN
        self.gps_data = NaN
        self.gps_data_old = NaN

        self.imu_changed = False
        self.gps_changed = False

        self.speed = 0.0
        self.climb = 0

        self.latitude = 0
        self.longitude = 0

        self.altitude = 0
        self.pressure_ref = 0

        self.gyro_scaled_x = 0
        self.gyro_scaled_y = 0
        self.gyro_scaled_z = 0
        self.accel_scaled_x = 0
        self.accel_scaled_y = 0
        self.accel_scaled_z = 0

        self.temperature = 0

        self.track = 0
        self.mode = 0
        self.nb_sats = 0

        self.pitch = 0
        self.roll = 0
        self.yaw = 0

    def set_config(self, config_file):
        config = ConfigParser.RawConfigParser()

        if os.path.exists(config_file):
            config.read(config_file)

            self.to_stdout = config.getboolean('general', 'to_stdout')
            self.front_axe = config.get('general', 'front_axe')

            self.sim = config.getboolean('simulation', 'sim')

            self.print_header = config.getboolean('file', 'print_header')
            self.path = config.get('file', 'path')
            self.filename = config.get('file', 'filename')

            self.wait_gps = config.getboolean('gps', 'wait_gps')
            self.nb_min_sat = config.getint('gps', 'nb_min_sat')
            self.autoset_time = config.getboolean('gps', 'autoset_time')

            self.north_offset = config.getint('compass', 'north_offset')

        else:
            print("No config file found for position recorder at " + config_file + ". Default config loaded.")

            self.to_stdout = False
            self.front_axe = 'y'

            self.sim = False

            self.print_header = True
            self.path = 'records/'
            self.filename = 'data_pos.csv'

            self.wait_gps = True
            self.nb_min_sat = 3
            self.autoset_time = True

            self.north_offset = 0

    def run(self):
        self.running = True

        speeds = []
        times = []

        if self.wait_gps:
            # Wait for GFS fix
            print("Waiting for GPS fix")
            while not self.gps_fixed and self.running:
                time.sleep(1)

                if self.gps.is_new_data():
                    self.gps_data = self.gps.get_data()
                    if self.gps_data.nb_sats >= self.nb_min_sat:
                        self.gps_fixed = True
                    else:
                        print(" > Only " + str(self.gps_data.nb_sats) + " sats")

            print("GPS fixed")

            if self.autoset_time:
                print("Setting board time with GPS time (UTC)")
                _linux_set_time(self.gps_data.time)
                print("Board time is now " + datetime.datetime.fromtimestamp(time.time()).strftime('%d.%m.%Y %H:%M:%S'))

        if self.print_header:
            self.writer.writerow([
                "time",
                "pitch", "roll", "yaw",
                "speed", "climb",
                "lat", "lon",
                "alt", "temp",
                "track", "mode", "sats",
                "gyro_scaled_x", "gyro_scaled_y", "gyro_scaled_z",
                "accel_scaled_x", "accel_scaled_y", "accel_scaled_z"
            ])

        self.imu_data = self.imu.get_data()
        self.gps_data = self.gps.get_data()

        self.time = self.gps_data.time
        self.gps_time = self.gps_data.time
        self.imu_time = self.imu_data.time

        time_offset = time.time()-self.gps_time

        while self.running:

            if self.sim:
                sim_time = time.time() - time_offset

                self.imu.set_sim_time(sim_time)
                self.gps.set_sim_time(sim_time)

            # Read data from sensors
            imu_new = self.imu.is_new_data()
            gps_new = self.gps.is_new_data()

            # If we got no new data, sleep a bit so we don't overload CPU
            if not imu_new and not gps_new:
                sleep(0.01)
                continue

            if imu_new:
                self.imu_data_old = self.imu_data
                self.imu_data = self.imu.get_data()

            if gps_new:
                self.gps_data_old = self.gps_data
                self.gps_data = self.gps.get_data()

            if imu_new:
                if self.front_axe == 'y':
                    self.roll = self.imu_data.roll*RAD_TO_DEG
                    self.pitch = self.imu_data.pitch*RAD_TO_DEG
                else:
                    if self.front_axe == 'x':
                        self.roll = self.imu_data.pitch*RAD_TO_DEG
                        self.pitch = self.imu_data.roll*RAD_TO_DEG
                    else:
                        print("Error, " + self.front_axe + " is not a valid front axe, put x or y")

                self.yaw = self.imu_data.yaw*RAD_TO_DEG+self.north_offset

                self.gyro_scaled_x = self.imu_data.gyro_scaled_x
                self.gyro_scaled_y = self.imu_data.gyro_scaled_y
                self.gyro_scaled_z = self.imu_data.gyro_scaled_z

                self.accel_scaled_x = self.imu_data.accel_scaled_x
                self.accel_scaled_y = self.imu_data.accel_scaled_y
                self.accel_scaled_z = self.imu_data.accel_scaled_z

                self.temperature = self.imu_data.temperature

            # Compute final data
            if gps_new:
                self.gps_data = self.gps.get_data()

                self.time = self.gps_data.time
                self.gps_time = self.time

                self.speed = self.gps_data.speed*MPS_TO_KPH
                self.climb = self.gps_data.climb*MPS_TO_KPH

                self.latitude = self.gps_data.latitude
                self.longitude = self.gps_data.longitude

                self.altitude = self.gps_data.altitude
                self.pressure_ref = self.imu_data.pressure

                self.track = self.gps_data.track
                self.mode = self.gps_data.mode
                self.nb_sats = self.gps_data.nb_sats

            else:
                if imu_new:

                    imu_time_delta = self.imu_data.time - self.imu_time
                    self.imu_time = self.imu_data.time

                    self.time += imu_time_delta

                    self.speed += (self.accel_scaled_y-abs(90-abs(self.pitch))/90)*imu_time_delta*MPS_TO_KPH
                    self.climb += self.accel_scaled_z*imu_time_delta*MPS_TO_KPH

                    self.altitude = self.gps_data.altitude + (self.imu_data.pressure-self.pressure_ref)*8

            # Write data line to CSV file
            self.writer.writerow([
                self.time,
                self.pitch, self.roll, self.yaw,
                self.speed, self.climb,
                self.latitude, self.longitude,
                self.altitude, self.temperature,
                self.track, self.mode, self.nb_sats,
                self.gyro_scaled_x, self.gyro_scaled_y, self.gyro_scaled_z,
                self.accel_scaled_x, self.accel_scaled_y, self.accel_scaled_z
            ])
            self.output.flush() # In live show using this is essential to avoid 1 sec buffering

    def stop(self):
        self.running = False

        self.imu.stop()
        self.gps.stop()


def _linux_set_time(timestamp):
    import ctypes
    import ctypes.util

    # /usr/include/linux/time.h:
    #
    # define CLOCK_REALTIME                     0
    CLOCK_REALTIME = 0

    # /usr/include/time.h
    #
    # struct timespec
    #  {
    #    __time_t tv_sec;            /* Seconds.  */
    #    long int tv_nsec;           /* Nanoseconds.  */
    #  };
    class timespec(ctypes.Structure):
        _fields_ = [("tv_sec", ctypes.c_long),
                    ("tv_nsec", ctypes.c_long)]

    librt = ctypes.CDLL(ctypes.util.find_library("rt"))

    ts = timespec()
    ts.tv_sec = int(timestamp)
    ts.tv_nsec = 0 # Millisecond to nanosecond

    # http://linux.die.net/man/3/clock_settime
    librt.clock_settime(CLOCK_REALTIME, ctypes.byref(ts))