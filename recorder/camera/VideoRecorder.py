import picamera
import threading
import ConfigParser
import os


class VideoRecorder(threading.Thread):

    def __init__(self, filename):
        threading.Thread.__init__(self)
        self.camera = picamera.PiCamera()

        self.resolution_x = 1280
        self.resolution_y = 720
        self.rotation = 0

        self.read_config()

        self.camera.resolution = (self.resolution_x, self.resolution_y)
        self.camera.rotation = self.rotation
        self.output = filename
        self.running = False
        
    def run(self):
        self.running = True

        self.camera.start_recording(self.output)

        while self.running:
            self.camera.wait_recording(1)

    def stop(self):
        self.running = False
        self.camera.stop_recording()

    def read_config(self):
        config = ConfigParser.RawConfigParser()
        config_file = 'config/camera.cfg'

        if os.path.exists(config_file):
            config.read(config_file)
            self.resolution_x = config.getint('camera', 'resolution_x')
            self.resolution_y = config.getint('camera', 'resolution_y')
            self.rotation = config.getint('camera', 'rotation')
        else:
            print("No camera config found, using default config.")

        print("Camera config :")
        print("- resolution : " + str(self.resolution_x) + "x" + str(self.resolution_y))
        print("- rotation : " + str(self.rotation) + "°")