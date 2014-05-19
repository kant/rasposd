import time
import os
import sys
import uuid

DOSSIER_COURRANT = os.path.dirname(os.path.abspath(__file__))
DOSSIER_PARENT = os.path.dirname(DOSSIER_COURRANT)
sys.path.append(DOSSIER_PARENT)

import position.PositionRecorder as PositionRecorder
import camera.VideoRecorder as VideoRecorder


directory = "records/record_" + str(time.time()) + "_" + str(uuid.uuid1()) + "/"

if not os.path.exists(directory):
    os.makedirs(directory)


pos = PositionRecorder.PositionRecorder(directory)
#video = VideoRecorder.VideoRecorder(directory + "video.h264")

try:
    print "Starting position recorder"
    pos.start()
    print "Starting video recorder"
    #video.start()

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
    #video.stop()
    pos.stop()

    #wait for the tread to finish
    print "- Wait for video recorder"
    #video.join()
    print "- Wait for position recorder"
    pos.join()

    print "Finished"
