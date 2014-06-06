import smbus
import threading
import time

from position.IMURecord import IMURecord

from position.bitify.python.sensors.gy88 import GY88
from position.bitify.python.utils.i2cutils import i2c_raspberry_pi_bus_number
from xml.etree.ElementPath import _SelectorContext


gyro_address = 0x68
compass_address = 0x1e
barometer_address = 0x77


class ImuDataset:

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


class ImuReader(threading.Thread):

    def __init__(self, magnetometer_calibration, freq,
                 obj_x, obj_y, obj_z, reverse):
        threading.Thread.__init__(self)

        self.bus = smbus.SMBus(i2c_raspberry_pi_bus_number())
        self.imu = GY88(self.bus, gyro_address, compass_address, barometer_address, "GY88", magnetometer_calibration,
                        obj_x, obj_y, obj_z, reverse)

        self.running = False
        self.data_set = ImuDataset()
        self.new = False

        self.period = 1/freq

    def run(self):
        self.running = True

        while self.running:
            self.data_set.set(self.imu.read_all())
            self.new = True

            time.sleep(self.period)

    def stop(self):
        self.running = False

    def is_new_data(self):
        was_new = self.new
        self.new = False
        return was_new

    def get_data(self):
        return self.data_set

    def set_sim_time(self, time):
        self.sim_time = time