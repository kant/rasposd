import picamera
import threading


class VideoRecorder(threading.Thread):

    def __init__(self, filename):
        threading.Thread.__init__(self)
        self.camera = picamera.PiCamera()
        self.camera.resolution = (1280, 720)
        self.output = filename
        self.running = False

    def run(self):
        self.running = True

        self.camera.start_recording(self.output)

        while self.running:
            self.camera.wait_recording(1)

        self.camera.stop_recording()

    def stop(self):
        self.running = False
