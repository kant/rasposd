import time
import os
import sys
import uuid

DOSSIER_COURRANT = os.path.dirname(os.path.abspath(__file__))
DOSSIER_PARENT = os.path.dirname(DOSSIER_COURRANT)
sys.path.append(DOSSIER_PARENT)

import position.GPSRecorder as GPSRecorder
import position.IMURecorder as IMURecorder
import camera.VideoRecorder as VideoRecorder


subdir = "record_" + str(time.time()) + "_" + str(uuid.uuid1()) + "/"
directory = "records/" + subdir

if not os.path.exists(directory):
    os.makedirs(directory)

os.remove('records/last')
os.symlink(subdir, 'records/last')


imu = IMURecorder.ImuRecorder(directory)
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
