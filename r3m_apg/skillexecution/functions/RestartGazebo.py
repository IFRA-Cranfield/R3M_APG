#!/usr/bin/python3

# # # # # # # # # # # # # # # # # #                                  
#                                 #
#   ===== COPYRIGHT HERE =====    #
#                                 #
# # # # # # # # # # # # # # # # # #

# ========================================================================================= #
# ======================================== INCLUDE ======================================== #
# ========================================================================================= #

# System:
import os, subprocess, time

# ROS2:
import rclpy
from rclpy.node import Node
from rcl_interfaces.msg import Log

# Global variable -> LAUNCH_COMPLETE:
GzLAUNCH_COMPLETE = False

# ========================================================================================= #
# =================================== CLASSES/FUNCTIONS =================================== #
# ========================================================================================= #

class LaunchSUB(Node):

    def __init__(self):
        
        # Declare NODE:
        super().__init__("R3MAPG_LaunchSUB")

        # Declare SUBSCRIBER:
        self.subscription = self.create_subscription(
            Log,                                                                                              
            "rosout",                                                        
            self.sub_callback,                                          
            10)                                                               
        self.subscription 
    
    def sub_callback(self, MSG):

        global GzLAUNCH_COMPLETE
    
        ROSout_msg = str(MSG.msg)
        
        if "Service response received for initialization" in ROSout_msg:
            GzLAUNCH_COMPLETE = True

def GAZEBO_start(PKG, CNF):

    SUBNode = LaunchSUB()
    global GzLAUNCH_COMPLETE

    CMD = "gnome-terminal -- ros2 launch ros2srrc_launch moveit2.launch.py package:=" + PKG + " config:=" + CNF
    
    print("")
    print("[GAZEBO START]: Executing command -> " + CMD)
    
    PROCESS = subprocess.Popen(CMD, shell=True)
    GzLAUNCH_COMPLETE = False

    print("[GAZEBO START]: Checking if Gz environment has been successfully launched...")

    T = time.time()

    while (time.time() < T + 30.0):
        rclpy.spin_once(SUBNode)
        if GzLAUNCH_COMPLETE:
            SUBNode.destroy_node()
            del SUBNode
            
            print("[GAZEBO START]: Gazebo successfully launched!")
            print("")
            return(True)

    SUBNode.destroy_node()
    del SUBNode
    
    print("[GAZEBO START]: ERROR -> Gz launch unsuccessful.")
    print("")
    return(False)

def GAZEBO_close():

    os.system("pkill -f gzclient")  
    os.system("pkill -f gzserver")  
    os.system("pkill -f robot_state_publisher")  
    os.system("pkill -f static_transform_publisher") 
    os.system("pkill -f move_group") 
    os.system("pkill -f move") 
    os.system("pkill -f robmove") 
    os.system("pkill -f robpose")
    os.system("pkill -f sequence") 
    os.system("pkill -f rviz2") 

def GAZEBO_REstart(PKG, CNF):

    print("")
    print("[GAZEBO RE-START]: Re-start of Gazebo environment requested.")

    print("[GAZEBO RE-START]: Closing current Gazebo window...")
    GAZEBO_close()
    print("[GAZEBO RE-START]: Gz window closed.")
    
    time.sleep(10.0)
    
    print("[GAZEBO RE-START]: Starting a new Gazebo environment...")
    RES = GAZEBO_start(PKG, CNF)
    
    return(RES)