from picamera2 import Picamera2, Preview
import libcamera
import time
picam2 = Picamera2()
camera_config = picam2.create_still_configuration(main={"size": (1920, 1080)}, lores={"size": (640, 480)}, display="lores")
# Add transform to rotate the image by 180 degrees
camera_config["transform"] = libcamera.Transform(hflip=1, vflip=1)
picam2.configure(camera_config)
picam2.start_preview(Preview.QTGL)
picam2.start()
# time.sleep(2)
# picam2.capture_file("test.jpg")
time.sleep(60)
