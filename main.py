import threading
import mavlink_monitor 
from Walking.Walking_RP_Code import walking_main
from camera import camera_main


if __name__ == "__main__":
  # Thread the functions to run both at the same time independent of one another
  mavlink_thread = threading.Thread(target=mavlink_monitor.mavlink_monitor)
  mavlink_thread.daemon = True
  mavlink_thread.start()

  walking_thread = threading.Thread(target=walking_main)
  walking_thread.daemon = True
  walking_thread.start()

  camera_thread = threading.Thread(target=camera_main)
  camera_thread.daemon = True
  # camera_thread.start()

  # Add these lines to make the main thread wait for them to finish 
  mavlink_thread.join()  
  walking_thread.join() 
  # camera_thread.join()
