#!/usr/bin/env python

import time
import picamera

with picamera.PiCamera() as camera:
    camera.resolution = (1296, 730)
    camera.framerate = 30
    camera.start_preview()
    time.sleep(500)
    camera.stop_preview()
