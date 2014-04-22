import smbus
import csv
import threading

from position.bitify.python.sensors.gy88 import GY88
from position.bitify.python.utils.i2cutils import i2c_raspberry_pi_bus_number

gyro_address = 0x68
compass_address = 0x1e
barometer_address = 0x77


class ImuRecorder(threading.Thread):

    def __init__(self, directory):
        threading.Thread.__init__(self)
        self.bus = smbus.SMBus(i2c_raspberry_pi_bus_number())
        self.imu = GY88(self.bus, gyro_address, compass_address, barometer_address, "GY88")
        self.output = open(directory + 'data_imu.csv', "wb")
        self.writer = csv.writer(self.output, delimiter='\t', quotechar='"', quoting=csv.QUOTE_NONNUMERIC)
        self.running = False

    def run(self):
        self.running = True

        self.writer.writerow([
            "mesure_time",
            "pitch", "roll", "yaw",
            "gyro_scaled_x", "gyro_scaled_y", "gyro_scaled_z",
            "accel_raw_x", "accel_raw_y", "accel_raw_z",
            "accel_scaled_x", "accel_scaled_y", "accel_scaled_z",
            "temperature", "pressure"
        ])

        while self.running:
            self.writer.writerow(self.imu.read_all())

    def stop(self):
        self.running = False
