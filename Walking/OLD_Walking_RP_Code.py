##  Authors: Alaa Osman, Trevor Tang, and Anthony Saldutti
##  Other partners: Spencer Schutz and Joe Zakielarz
##  Organization: Duke University, Mechanical Engineering
##
##  This script was adapted from Ethan Lipson's hello_world.py script (git@github.com:ethanlipson/PyLX-16A.git) \\
##  for the LX-16A motors.
##
##  Its purpose is to execute the walking functionality of our senior capstone project (Wallking and Flying Robot), a \\
##  quadruped done. Said robot moves forwards or back, and the legs can extend or tuck under the body for flying mode.
##
##  Last modified: April 16, 2024

############################################################################################################################


# Importing modules.

from math import sin, cos   # To do math.
from lx16a import *         # To control the servos.
import time                 # To track time for delays or walking patterns.
import threading            # To run different sections of code concurently.

# Initialize the servo controller, connect to the servos, and set their angle limits.

LX16A.initialize("/dev/ttyUSB0", 0.1)

try:
    servo1 = LX16A(1)
    servo2 = LX16A(2)
    servo3 = LX16A(3)
    servo4 = LX16A(4)
    servo5 = LX16A(5)
    servo6 = LX16A(6)
    servo7 = LX16A(7)
    servo8 = LX16A(8)

    # The motors' angular positions physcially can only go from 0 to 240 degrees.
    servo1.set_angle_limits(0, 240)
    time.sleep(0.5)
    servo2.set_angle_limits(0, 240)
    time.sleep(0.5)
    servo3.set_angle_limits(0, 240)
    time.sleep(0.5)
    servo4.set_angle_limits(0, 240)
    time.sleep(0.5)
    servo5.set_angle_limits(0, 240)
    time.sleep(0.5)
    servo6.set_angle_limits(0, 240)
    time.sleep(0.5)
    servo7.set_angle_limits(0, 240)
    time.sleep(0.5)
    servo8.set_angle_limits(0, 240)
    time.sleep(0.5)
    
# If a specific servo is not responding, exit from the code.
# There is an issue (e.g., disconnected cable, violated voltage limits, overheating, etc.)

except ServoTimeoutError as e:
    print(f"Servo {e.id_} is not responding. Exiting...")
    quit()

# Read the angular positions of each servo.

def read_angles():
    
    print("Current Servo Angles: ")
    for servo in [servo1, servo2, servo3, servo4, servo5, servo6, servo7, servo8]:
        print(servo.get_physical_angle())
    print("\n")

# Make the robot stand in place.

def stand():

    print("Standing.")

    ### Upper motors.
    servo1.move(37.20, 1000)
    servo3.move(147.84, 1000)
    servo5.move(118.32, 1000)
    servo7.move(117, 1000)
    time.sleep(1.5)
    ### Lower motors.
    servo2.move(150.96, 1000)
    servo4.move(108, 1000)
    servo6.move(50.88, 1000)
    servo8.move(106, 1000)
    time.sleep(2)

# Make the robot tuck its legs undenreath the body.
# Use for flying mode.

def land():

    print('Landing')
    print('\n')
    ## Lower motors
    servo2.move(104.16, 1000)
    servo4.move(49.92, 1000)
    servo6.move(7.68, 1000)
    servo8.move(64, 1000)
    time.sleep(1.5)
    ## Upper motors
    servo1.move(4.32, 1000)
    servo3.move(111.6, 1000)
    servo5.move(85.92, 1000)
    servo7.move(52.32, 1000)
    time.sleep(2)


#   Make the robot walk by each of the four legs in regular, timed patterns.
##  This function takes three parameters, which are physically set by a remote controller \\
##  connected to our microcontroller (a Raspberry Pi 4B):
##      1. walking_lock: Boolean determining whether the code runs (True) or no (False)
##      2. walking_direction: Value determining which direction the robot moves (front, middle/standing, or back)
##      3. walking_speed: Float determining the speed of the robot (by uniformly scaling servo rotation times and delays)

def walk(walking_lock = False, walking_direction = 'forward', walking_speed=1):

    global stop_flag

    stand()

    # If the walking function is locked, don't walk! (Duh).
    
    if walking_lock:
        print("Walking is locked--no bueno.")

    # The robot can walk if the walking function isn't locked.
    
    else:

        try :
            # In the "forward" direction, motors 1-4 are in the front.
            if walking_direction == 'forward':

                print('Moving forward')
                while True:
                    positions = [
                        (50, 150, 197, 24, 108, 42, 122, 105),  # Step 1
                        (37, 130, 197, 99, 118, 65, 122, 55),   # Step 2
                        (75, 81, 168, 90, 130, 56, 85, 90),     # Step 3
                        (75, 152, 157, 73, 130, 10, 95, 112),   # Step 4
                    ]
                    for pos in positions:
                        try:
                            servo1.move(pos[0], int(1000/walking_speed))
                            servo2.move(pos[1], int(1000/walking_speed))
                            servo3.move(pos[2], int(1000/walking_speed))
                            servo4.move(pos[3], int(1000/walking_speed))
                            servo5.move(pos[4], int(1000/walking_speed))
                            servo6.move(pos[5], int(1000/walking_speed))
                            servo7.move(pos[6], int(1000/walking_speed))
                            servo8.move(pos[7], int(1000/walking_speed))

                            time.sleep(0.8/walking_speed)

                            if stop_flag:
                                return
                        except KeyboardInterrupt:
                            stop_flag = True
                            print("Walk interrupted by user.")
                            return

        # The "middle" direction is just the robot standing in place.
        
            elif walking_direction == 'middle':

                print('Staying in place')
                stand()

        # In the "backward" direction, motors 5-8 are in the front instead.

            elif walking_direction == 'backward':

                print('Moving backward--still in progress!') # We still need to figure this out.

        except Exception as e:
            print(f"An error occurred: {e}")
            
 # Initialize stop_flag before main()
stop_flag = False


# Gets a boolean input from the user.

def get_boolean_input(prompt):
    
    #Gets boolean input from the user.
    while True:
        user_input = input(prompt).strip().lower()
        if user_input == 'true':
            return True
        elif user_input == 'false':
            return False
        else:
            print("Invalid input. Please enter 'true' or 'false'.")

# Prompts the users for walking parameters (runs before actually walking).

def walk_prompt():
    
    walking_lock = get_boolean_input("Enter walking lock status (True/False): ")
    walking_direction = input("Enter walking direction (forward/backward): ").lower()
    walking_speed = float(input("Enter walking speed: "))
    walk(walking_lock, walking_direction, walking_speed)

# Handles the user input.

def handle_user_input(key_press):

    actions = {
        'r': read_angles,
        's': stand,
        'l': land,
        'w': walk_prompt,
    }
    action = actions.get(key_press)
    if action:
        action()
    else:
        print("Invalid input.")

# Really just for for taking keyboard inputs from the user.

def walking_main():
    """Main function to handle user input."""
    while True:
        key_press = input("Press 'r' to read angles, 's' to stand, 'l' to land, 'w' to start walking: ")
        handle_user_input(key_press)

