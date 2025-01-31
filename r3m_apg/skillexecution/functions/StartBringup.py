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
import os, subprocess, time, yaml
from ament_index_python.packages import get_package_share_directory

# ROS2:
import rclpy
from rclpy.node import Node
from rcl_interfaces.msg import Log

# Global variable -> LAUNCH_COMPLETE:
BrLAUNCH_COMPLETE = False

# ========================================================================================= #
# ================================ ROS2 - INPUT PARAMETERS ================================ #
# ========================================================================================= #

def GetROB_YAML(NAME):
    
    PATH = os.path.join(get_package_share_directory('r3m_apg'), 'apg', 'usecase')
    YAML_PATH = PATH + "/" + NAME + ".yaml"

    # Get VALUES:
    with open(YAML_PATH, 'r') as YAML:
        icYAML = yaml.safe_load(YAML)
    
    ROBOT = icYAML["Robot"]["Model"]

    return(ROBOT)

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

        global BrLAUNCH_COMPLETE
    
        ROSout_msg = str(MSG.msg)
        
        if "Service response received for initialization" in ROSout_msg:
            BrLAUNCH_COMPLETE = True

def BRINGUP_start(PKG, CNF, IP):

    # Get UseCase from yaml file:
    ROBOT = GetROB_YAML(CNF)

    SUBNode = LaunchSUB()
    global BrLAUNCH_COMPLETE

    if "ur" in ROBOT:
        CMD = "gnome-terminal -- ros2 launch ros2srrc_launch bringup_ur.launch.py package:=" + PKG + " config:=" + CNF + " robot_ip:=" + IP
    elif "irb" in ROBOT:
        CMD = "gnome-terminal -- ros2 launch ros2srrc_launch bringup_abb.launch.py package:=" + PKG + " config:=" + CNF + " robot_ip:=" + IP
    else:
        CMD = None
    
    print("")
    print("[ROBOT BRINGUP START]: Executing command -> " + CMD)
    
    PROCESS = subprocess.Popen(CMD, shell=True)
    BrLAUNCH_COMPLETE = False

    print("[ROBOT BRINGUP START]: Checking if RbBr environment has been successfully launched...")

    T = time.time()

    while (time.time() < T + 30.0):
        rclpy.spin_once(SUBNode)
        if BrLAUNCH_COMPLETE:
            SUBNode.destroy_node()
            del SUBNode
            
            print("[ROBOT BRINGUP START]: Robot Bringup successfully launched!")
            print("")
            return(True)

    SUBNode.destroy_node()
    del SUBNode
    
    print("[ROBOT BRINGUP START]: ERROR -> RbBr launch unsuccessful (TIMEOUT).")
    print("")
    return(False)

def BRINGUP_close():

    os.system("pkill -f ros2_control_node")  
    os.system("pkill -f robot_state_publisher")  
    os.system("pkill -f static_transform_publisher") 
    os.system("pkill -f move_group") 
    os.system("pkill -f move") 
    os.system("pkill -f robmove") 
    os.system("pkill -f robpose")
    os.system("pkill -f rviz2") 
    os.system("pkill -f ros2") 