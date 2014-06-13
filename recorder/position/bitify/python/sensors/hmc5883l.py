import math

import position.bitify.python.utils.i2cutils as I2CUtils
import time


class HMC5883L(object):
    '''
    Simple HMC5883L 3-Axis Digital Compass implementation
    '''
    TWO_PI = 2 * math.pi

    CONF_REG_A = 0
    CONF_REG_B = 1
    MODE_REG = 2
    DATA_START_BLOCK = 3
    DATA_XOUT_H = 0
    DATA_XOUT_L = 1
    DATA_ZOUT_H = 2
    DATA_ZOUT_L = 3
    DATA_YOUT_H = 4
    DATA_YOUT_L = 5

    SAMPLE_RATE = { 0 : 0.75, 1 : 1.5, 2 : 3, 3 : 7.5, 4 : 15, 5 : 30, 6 : 75, 7 :-1 }

    SAMPLE_MODE = { 0 : "CONTINUOUS", 1 : "SINGLE", 2 : "IDLE", 3 : "IDLE" }

    GAIN_SCALE = {
                    0 : [ 0.88, 1370, 0.73 ],
                    1 : [ 1.30, 1090, 0.92 ],
                    2 : [ 1.90, 820, 1.22 ],
                    3 : [ 2.50, 660, 1.52 ],
                    4 : [ 4.00, 440, 2.27 ],
                    5 : [ 4.70, 390, 2.56 ],
                    6 : [ 5.60, 330, 3.03 ],
                    7 : [ 8.10, 230, 4.35 ]
                 }

    def __init__(self, bus, address, name, samples=3, rate=6, gain=1, sampling_mode=0,
                 x_offset=0, y_offset=0, z_offset=0,
                 obj_x='x', obj_y='y', obj_z='z',
                 reverse=False):
        self.bus = bus
        self.address = address
        self.name = name
        self.samples = samples
        self.gain = gain
        self.sampling_mode = sampling_mode
	self.rate = rate
        
        self.x_offset = x_offset
        self.y_offset = y_offset
        self.z_offset = z_offset

        self.obj_x = obj_x
        self.obj_y = obj_y
        self.obj_z = obj_z

        self.scaled_x = 0
        self.scaled_y = 0
        self.scaled_z = 0
	
	self.init = 10

        if reverse:
            self.reverse = -1
        else:
            self.reverse = 1

        try:
            self.hw_init(samples, rate, gain)
        except IOError:
            try:
                print("Compass hardware init failed, trying again")
                self.hw_init(samples, rate, gain)
                print("Hardware init OK")
            except IOError:
                print("Hardware init failed twice, your power supply may be too weak. Please run again.")
                return

        self.raw_data = [0, 0, 0, 0, 0, 0]
        
        # Now read all the values as the first read after a gain change returns the old value
        self.read_raw_data()

    def hw_init(self, samples, rate, gain):
        # Set the number of samples
        conf_a = (samples << 5) + (rate << 2)
        I2CUtils.i2c_write_byte(self.bus, self.address, HMC5883L.CONF_REG_A, conf_a)

        # Set the gain
        conf_b = gain << 5
        I2CUtils.i2c_write_byte(self.bus, self.address, HMC5883L.CONF_REG_B, conf_b)

        # Set the operation mode
        I2CUtils.i2c_write_byte(self.bus, self.address, HMC5883L.MODE_REG, self.sampling_mode)

    def get_axis(self, data, axis):
        return {
            'x': I2CUtils.twos_compliment(data[HMC5883L.DATA_XOUT_H], data[HMC5883L.DATA_XOUT_L]) - self.x_offset,
            'y': I2CUtils.twos_compliment(data[HMC5883L.DATA_YOUT_H], data[HMC5883L.DATA_YOUT_L]) - self.y_offset,
            'z': I2CUtils.twos_compliment(data[HMC5883L.DATA_ZOUT_H], data[HMC5883L.DATA_ZOUT_L]) - self.z_offset
            }.get(axis, 0)

    def read_raw_data(self):
        '''
        Read the raw data from the sensor, scale it appropriately and store for later use
        '''
        try:
            self.raw_data = I2CUtils.i2c_read_block(self.bus, self.address, HMC5883L.DATA_START_BLOCK, 6)
            self.raw_x = self.get_axis(self.raw_data, self.obj_x)*self.reverse
            self.raw_y = self.get_axis(self.raw_data, self.obj_y)
            self.raw_z = self.get_axis(self.raw_data, self.obj_z)*self.reverse

            self.distance = abs(self.scaled_x - self.raw_x * HMC5883L.GAIN_SCALE[self.gain][2])
            self.distance += abs(self.scaled_y - self.raw_y * HMC5883L.GAIN_SCALE[self.gain][2])
            self.distance += abs(self.scaled_z - self.raw_z * HMC5883L.GAIN_SCALE[self.gain][2])
            # print("magnetic_distance _ " + str(self.distance) )
            # print("magnetique _" + str(self.raw_x) + "_"+ str(self.raw_y) + "_" + str(self.raw_z) ) 

            if (self.distance < 500) or (self.init > 0):
		self.init -= 1
		if self.init < 0:
                    self.init = 0
                # print("ok")
                # add a filter on the datas
                self.scaled_x = 0.9 * self.scaled_x + 0.1 * self.raw_x * HMC5883L.GAIN_SCALE[self.gain][2]
                self.scaled_y = 0.9 * self.scaled_y + 0.1 * self.raw_y * HMC5883L.GAIN_SCALE[self.gain][2]
                self.scaled_z = 0.9 * self.scaled_z + 0.1 * self.raw_z * HMC5883L.GAIN_SCALE[self.gain][2]
            else: # les donnees sont corrompu
                self.hw_init(self.samples, self.rate, self.gain)
		# time.sleep(1)
		self.init = 10

        except IOError:
            print("Error reading compass, data ignored")

    def read_bearing(self):
        '''
        Read a bearing from the sensor assuming the sensor is level
        '''
        self.read_raw_data()

        bearing = math.atan2(self.read_scaled_y(), self.read_scaled_x())
        if bearing < 0:
            return bearing + (HMC5883L.TWO_PI)
        else:
            return bearing

    def read_compensated_bearing(self, pitch, roll):
        '''
        Calculate a bearing taking in to account the current pitch and roll of the device as supplied as parameters
        '''
        # self.read_raw_data()
	# we already have new data
        # print("magnetique _" + str(self.read_scaled_x()) + "_"+ str(self.read_scaled_y()) + "_" + str(self.read_scaled_z()) ) 
        cos_pitch = (math.cos(pitch))
        sin_pitch = (math.sin(pitch))
        
        cos_roll = (math.cos(roll))
        sin_roll = (math.sin(roll))
    
        Xh = (self.scaled_x * cos_roll) + (self.scaled_z * sin_roll)
        Yh = (self.scaled_x * sin_pitch * sin_roll) + (self.scaled_y * cos_pitch) - (self.scaled_z * sin_pitch * cos_roll)
        
        bearing = math.atan2(Yh, Xh)
        if bearing < 0:
            return bearing + (HMC5883L.TWO_PI)
        else:
            return bearing
    
    def set_offsets(self, x_offset, y_offset, z_offset):
        self.x_offset = x_offset
        self.y_offset = y_offset
        self.z_offset = z_offset
    
    def read_raw_x(self):
        return self.raw_x
    
    def read_raw_y(self):
        return self.raw_y
    
    def read_raw_z(self):
        return self.raw_z

    def read_scaled_x(self):
        return self.scaled_x

    def read_scaled_y(self):
        return self.scaled_y

    def read_scaled_z(self):
        return self.scaled_z
    
    def get_calibration(self):
        minx = 0
        maxx = 0
        miny = 0
        maxy = 0
        minz = 0
        maxz = 0

        for i in range(0,1000):

            raw_data = I2CUtils.i2c_read_block(self.bus, self.address, HMC5883L.DATA_START_BLOCK, 6)
            x_out = self.get_axis(raw_data, self.obj_x)
            y_out = self.get_axis(raw_data, self.obj_y)
            z_out = self.get_axis(raw_data, self.obj_z)

            if x_out < minx:
                minx=x_out

            if y_out < miny:
                miny=y_out

            if z_out < minz:
                minz=z_out

            if x_out > maxx:
                maxx=x_out

            if y_out > maxy:
                maxy=y_out

            if z_out > maxz:
                maxz=z_out


            #print x_out, y_out, (x_out * scale), (y_out * scale)
            time.sleep(0.1)


        x_offset = (maxx + minx) / 2
        y_offset = (maxy + miny) / 2
        z_offset = (maxz + minz) / 2

        return [x_offset, y_offset, z_offset]
