from picamera2 import Picamera2, Preview
import libcamera
import time
import os

picam2 = Picamera2()
camera_config = picam2.create_still_configuration(main={"size": (1920, 1080)}, lores={"size": (640, 480)}, display="lores")
# Add transform to rotate the image by 180 degrees
camera_config["transform"] = libcamera.Transform(hflip=1, vflip=1)
picam2.configure(camera_config)
picam2.start()



def camera_main():
  while True:
    timestamp = time.strftime("%Y%m%d_%H%M%S")
    filename = f"wfr_{timestamp}.jpg"
    folder_path = "/home/wfr/Walking-and-Flying-Robot/images"
    file_path = os.path.join(folder_path, filename)
    picam2.capture_file(file_path)
    print(f"Picture taken! Filename: {file_path}")
    time.sleep(10)