#!/usr/bin/env python

import smbus

import web  # web.py
import bitify.python.sensors.gy88 as GY88
from bitify.python.utils.i2cutils import i2c_raspberry_pi_bus_number


urls = (
    '/', 'index'
)

bus = smbus.SMBus(i2c_raspberry_pi_bus_number())

gyro_address = 0x68
compass_address = 0x1e
barometer_address = 0x77

imu_controller = GY88.GY88(bus, gyro_address, compass_address, barometer_address, "GY88")
imu_controller.set_compass_offsets(9, -10, -140)

app = web.application(urls, globals())


class index:
    def GET(self):
        (time, pitch, roll, yaw, gyro_scaled_x, gyro_scaled_y, gyro_scaled_z,accel_scaled_x, accel_scaled_y, accel_scaled_z, temperature, pressure) = imu_controller.read_all()
        result = "%.2f %.2f %.2f" % (pitch, roll, yaw)
        return result

if __name__ == "__main__":
    app.run()
