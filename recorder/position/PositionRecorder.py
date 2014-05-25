from gps import *
import csv
import threading
import datetime

import GPSReader as GPSReader
import IMUReader as IMUReader
# import pylab

class PositionRecorder(threading.Thread):

    def __init__(self, directory, magnetometer_calibration):
        threading.Thread.__init__(self)

        self.sim = False

        self.imu = IMUReader.ImuReader(magnetometer_calibration, self.sim, 'records/feed/data_imu.csv')
        self.gps = GPSReader.GpsReader(self.sim, 'records/feed/data_gps.csv')

        self.imu.start()
        self.gps.start()

        self.output = open(directory + 'data_pos.csv', "wb")
        #self.output = open('/dev/stdout', "wb")
        self.writer = csv.writer(self.output, delimiter='\t', quotechar='"', quoting=csv.QUOTE_NONNUMERIC)
        self.running = False

        self.gps_fixed = False

        self.imu_data = NaN
        self.imu_data_old = NaN
        self.gps_data = NaN
        self.gps_data_old = NaN

        self.imu_changed = False
        self.gps_changed = False

        self.speed = 0
        self.climb = 0

        self.latitude = 0
        self.longitude = 0

        self.altitude = 0
        self.pressure_ref = 0

        self.temperature = 0

        self.track = 0
        self.mode = 0
        self.nb_sats = 0

        self.pitch = 0
        self.roll = 0
        self.yaw = 0

    def run(self):
        self.running = True

        speeds = []
        times = []


        # Wait for GFS fix
        print("Waiting for GPS fix")
        while not self.gps_fixed:
            time.sleep(1)

            if self.gps.is_new_data():
                self.gps_data = self.gps.get_data()
                if self.gps_data.nb_sats >= 3:
                    self.gps_fixed = True
                else:
                    print(" > Only " + str(self.gps_data.nb_sats) + " sats")

        print("GPS fixed")

        print("Setting board time with GPS time (UTC)")
        _linux_set_time(self.gps_data.time)
        print("Board time is now " + datetime.datetime.fromtimestamp(time.time()).strftime('%d.%m.%Y %H:%M:%S'))

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

        self.time = self.gps_data.time
        self.gps_time = self.gps_data.time
        self.imu_time = self.imu_data.time

        time_offset = time.time()-self.gps_time

        print("Time offset is : " + str(time_offset))

        # f = pylab.figure()
        # f.show()

        while self.running:

            if self.sim:
                sim_time = time.time() - time_offset

                self.imu.set_sim_time(sim_time)
                self.gps.set_sim_time(sim_time)

            # Read data from sensors
            imu_new = self.imu.is_new_data()
            gps_new = self.gps.is_new_data()

            # imu_new = False
            # gps_new = False

            if imu_new:
                self.imu_data_old = self.imu_data
                self.imu_data = self.imu.get_data()

            if gps_new:
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
                self.nb_sats = self.gps_data.nb_sats
            else:
                if imu_new:

                    imu_time_delta = self.imu_data.time - self.imu_time
                    self.imu_time = self.imu_data.time

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
                self.track, self.mode, self.nb_sats
            ])
            self.output.flush()

            speeds.append(self.speed)
            times.append(self.time)

            # f.set_ydata(speeds)
            # f.set_xdata(times)
            # pylab.plot(speeds)
            # pylab.draw()

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