import picamera
import threading
import ConfigParser
import os
import time


class VideoRecorder(threading.Thread):

    def __init__(self, filename):
        threading.Thread.__init__(self)
        self.camera = picamera.PiCamera()

        self.read_config()

        self.camera.resolution = (self.resolution_x, self.resolution_y)
        self.camera.rotation = self.rotation
        self.camera.preview_layer = 0
        self.output = filename
        self.running = False
        
    def run(self):

        if not self.enable_preview and not self.enable_record:
            return

        self.running = True

        if self.enable_preview:
            self.camera.start_preview()

        if self.enable_record:
            self.camera.start_recording(self.output)

        while self.running:
            if self.enable_preview:
                time.sleep(1)

            if self.enable_record:
                self.camera.wait_recording(1)

    def stop(self):
        self.running = False

        if self.enable_preview:
            self.camera.stop_preview()

        if self.enable_record:
            self.camera.stop_recording()

    def read_config(self):
        config = ConfigParser.RawConfigParser()
        config_file = 'config/camera.cfg'

        if os.path.exists(config_file):
            config.read(config_file)
            self.resolution_x = config.getint('camera', 'resolution_x')
            self.resolution_y = config.getint('camera', 'resolution_y')
            self.rotation = config.getint('camera', 'rotation')
            self.enable_preview = config.getboolean('camera', 'preview')
            self.enable_record = config.getboolean('camera', 'record')
        else:
            print("No camera config found, using default config.")
            self.resolution_x = 1280
            self.resolution_y = 720
            self.rotation = 0
            self.enable_preview = True
            self.enable_record = False

        print("Camera config :")
        print(" - resolution : " + str(self.resolution_x) + "x" + str(self.resolution_y))
        print(" - rotation : " + str(self.rotation) + " degrees")
        print(" - preview : " + str(self.enable_preview))
        print(" - record : " + str(self.enable_record))
