import time
import os
import sys
import uuid
import ConfigParser

DOSSIER_COURRANT = os.path.dirname(os.path.abspath(__file__))
DOSSIER_PARENT = os.path.dirname(DOSSIER_COURRANT)
sys.path.append(DOSSIER_PARENT)

import position.GPSRecorder as GPSRecorder
import position.IMURecorder as IMURecorder
import camera.VideoRecorder as VideoRecorder


# Define record folder and links
subdir = "record_" + str(time.time()) + "_" + str(uuid.uuid1()) + "/"
directory = "records/" + subdir

if not os.path.exists(directory):
    os.makedirs(directory)

last_dir = 'records/last'
if os.path.isdir(last_dir):
    os.remove(last_dir)
os.symlink(subdir, last_dir)


# Read calibration data
config = ConfigParser.RawConfigParser()
config_file = 'calibration/last.cfg'

magnetometer_calibration = [0] * 3

if os.path.exists(config_file):
    config.read(config_file)
    magnetometer_calibration[0] = config.getint('magnetometer', 'x_offset')
    magnetometer_calibration[1] = config.getint('magnetometer', 'y_offset')
    magnetometer_calibration[2] = config.getint('magnetometer', 'z_offset')
else:
    print("Your compass is not calibrated. Please run the calibration script for better performances. "
          "You should run it each time the device environment (magnetic noise) changed.")

imu = IMURecorder.ImuRecorder(directory, magnetometer_calibration)
gps = GPSRecorder.GpsRecorder(directory)
video = VideoRecorder.VideoRecorder(directory + "video.h264")

try:
    print "Starting IMU recorder"
    imu.start()
    print "Starting GPS recorder"
    gps.start()
    print "Starting video recorder"
    video.start()

    print "Now recording..."
    while True:
        time.sleep(5)

#Ctrl C
except KeyboardInterrupt:
    print "User cancelled"

#Error
except:
    print "Unexpected error"
    raise

finally:
    print "Stopping recorders"
    video.stop()
    gps.stop()
    imu.stop()

    #wait for the tread to finish
    print "- Wait for video recorder"
    video.join()
    print "- Wait for gps recorder"
    gps.join()
    print "- Wait for imu recorder"
    imu.join()

    print "Finished"
