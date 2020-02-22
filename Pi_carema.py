import time
import io
import threading
import picamera 

class Camera(object):

    thread = None  # background thread that reads frames from camera
    frame = None  # current frame is stored here by background thread
    take_pirture = False
    close_camera = True

    def initialize(self):

        with picamera.PiCamera() as camera :
            camera.resolution = (1024, 768)
            # camera setup
            camera.resolution = (320, 240)
            camera.hflip = True
            camera.vflip = True

            # let camera warm up
            camera.start_preview()
            time.sleep(2)


    def get_video_stream_job(self):
        #with picamera.PiCamera() as camera:
        stream = io.BytesIO()
        while (not self.close_camera):
            time.sleep(0)
        with picamera.PiCamera() as camera :
            self.close_camera = False
            for foo in camera.capture_continuous(stream, 'jpeg', use_video_port=True):
                # store frame
                stream.seek(0)
                self.frame = stream.read()

                # reset stream for next frame
                stream.seek(0)
                stream.truncate()

                if self.take_pirture:
                    camera.close()
                    self.close_camera = True 
                    break

        while self.take_pirture:
            time.sleep(1)

        self.thread = None
    
    def export_video_stream(self):
        if self.thread is None:
            # start background frame thread
            self.thread = threading.Thread(target=self.get_video_stream_job)
            self.thread.start()

            # wait until frames start to be available
            while self.frame is None:
                time.sleep(0)
        return self.frame

     
    def take_picture(self):
        self.take_pirture = True
        while (not self.close_camera):
            time.sleep(0)
        
        with picamera.PiCamera() as camera:
            self.close_camera = False
            picture_name = str(int(time.time())) + ".jpeg"
            camera.capture("picture/" + picture_name)

        self.take_pirture = False
        self.close_camera = True

        return picture_name


    def record_video(self):
        pass