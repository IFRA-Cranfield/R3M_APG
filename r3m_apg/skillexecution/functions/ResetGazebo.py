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
import xacro
import ast
import random

# ROS2:
import rclpy
from rclpy.node import Node
from rcl_interfaces.msg import Log
from ament_index_python.packages import get_package_share_directory

# ROS2 MSG/SRV/ACTION:
from gazebo_msgs.srv import SpawnEntity
from gazebo_msgs.srv import DeleteEntity

# CUSTOM ROS2 MSG/SRV/ACTION:
from ros2srrc_data.msg import Robpose
from ros2srrc_data.msg import Action
from ros2srrc_data.msg import Xyz

# VARIABLE for HomePos recovery:
ACTION = Action()
ACTION.action = "MoveL"
ACTION.speed = 0.1
INPUT = Xyz()
INPUT.z = 0.05
ACTION.movel = INPUT

# Global variable -> LAUNCH_COMPLETE:
GzLAUNCH_COMPLETE = False

# ========================================================================================= #
# =================================== CLASSES/FUNCTIONS =================================== #
# ========================================================================================= #

# ========================================================================================= #
# CLASS -> RESET GAZEBO:
class GzRESET():

    def __init__(self,  ResetCondition, ROBOT_CLIENT, EE_CLIENT):
        
        # InitialCondition: dict() with:
        # "Robot": {Model - Link - EEType - Package - InitialPose - HomePose}
        # "ObjectList": [{Name - Link - CADFile - Package - InitialPose - CurrentPose - PreviousPose}, ..]
        self.ResetCond = ResetCondition
        
        self.OLCheck = False
        if self.ResetCond["ObjectList"] != None:
            self.OLCheck = True

        # Initialise ROS2 Clients:
        self.ENTITY_CLIENT = EntityClient()
        self.ROBOT_CLIENT = ROBOT_CLIENT
        
        self.EEType = ResetCondition["Robot"]["EEType"]
        
        if self.EEType == "ParallelGripper":
            self.EE_CLIENT = EE_CLIENT
        elif self.EEType == "VacuumGripper":
            self.EE_CLIENT = EE_CLIENT
        
        if self.OLCheck:

            # Spawn OBJECTS IN INITIAL CONDITIONS:
            for x in self.ResetCond["ObjectList"]:

                self.ENTITY_CLIENT.spawn_REQUEST("OBJECT", x)
                while rclpy.ok():
                    rclpy.spin_once(self.ENTITY_CLIENT)
                    if self.ENTITY_CLIENT.future_SPAWN.done():
                        try:
                            spawnRES = self.ENTITY_CLIENT.future_SPAWN.result()
                        except Exception as exc:
                            self.ENTITY_CLIENT.get_logger().info("[R3M Cell] - /SpawnEntity ROS2 Service call failed. ERROR: " + str(exc))
                            return(False)
                        else:
                            self.ENTITY_CLIENT.get_logger().info("[R3M Cell] - /SpawnEntity RESULT: " + str(spawnRES.status_message))
                        break

    def RESET(self):
        
        # Reset End-Effector:
        if self.EEType == "ParallelGripper":
            self.EE_CLIENT.OPEN()
        elif self.EEType == "VacuumGripper":
            self.EE_CLIENT.DEACTIVATE()
            
        if self.OLCheck:
            
            # Delete any object that could be in the workspace:
            for x in self.ResetCond["ObjectList"]:

                self.ENTITY_CLIENT.delete_REQUEST("OBJECT", x)
                while rclpy.ok():
                    rclpy.spin_once(self.ENTITY_CLIENT)
                    if self.ENTITY_CLIENT.future_DELETE.done():
                        try:
                            deleteRES = self.ENTITY_CLIENT.future_DELETE.result()
                        except Exception as exc:
                            self.ENTITY_CLIENT.get_logger().info("[R3M Cell] - /DeleteEntity ROS2 Service call failed. ERROR: " + str(exc))
                            return(False)
                        else:
                            self.ENTITY_CLIENT.get_logger().info("[R3M Cell] - /DeleteEntity RESULT: " + str(deleteRES.status_message))
                        break

        # Reset Robot's position:
        HomePose = Robpose()
        HomePose.x = self.ResetCond["Robot"]["HomePose"]["x"]
        HomePose.y = self.ResetCond["Robot"]["HomePose"]["y"]
        HomePose.z = self.ResetCond["Robot"]["HomePose"]["z"]
        HomePose.qx = self.ResetCond["Robot"]["HomePose"]["qx"]
        HomePose.qy = self.ResetCond["Robot"]["HomePose"]["qy"]
        HomePose.qz = self.ResetCond["Robot"]["HomePose"]["qz"]
        HomePose.qw = self.ResetCond["Robot"]["HomePose"]["qw"]
        
        HP_RES = self.ROBOT_CLIENT.RobMove_EXECUTE("PTP", 1.0, HomePose)
        
        if HP_RES["Success"]:
            self.ENTITY_CLIENT.get_logger().info("[R3M Cell] - Robot moved back to HOME POSITION. Ready to start again!")
        else:
            self.ENTITY_CLIENT.get_logger().info("[R3M Cell] - ERROR moving the Robot directly back to HOME POSITION. Trying SafePose...")
            
            RECOVERED = False
            for x in self.ResetCond["Robot"]["SafePose"]:
                
                SafePose = Robpose()
                SafePose.x = x["x"]
                SafePose.y = x["y"]
                SafePose.z = x["z"]
                SafePose.qx = x["qx"]
                SafePose.qy = x["qy"]
                SafePose.qz = x["qz"]
                SafePose.qw = x["qw"]
                
                SP_RES = self.ROBOT_CLIENT.RobMove_EXECUTE("LIN", 0.1, SafePose)
                if SP_RES["Success"]:
                    
                    HP_RES = self.ROBOT_CLIENT.RobMove_EXECUTE("PTP", 1.0, HomePose)
                    if HP_RES["Success"]:
                        self.ENTITY_CLIENT.get_logger().info("[R3M Cell] - Robot moved back to HOME POSITION. Ready to start again!")
                        
                        RECOVERED = True
                        break
                    else:
                        None # Try again.
                        
            if RECOVERED == False:
                self.ENTITY_CLIENT.get_logger().info("[R3M Cell] - ERROR moving the Robot back to HOME POSITION in RESET.")   
                return(False)
        
        if self.OLCheck:
        
            # Spawn the OBJECTS back:
            for x in self.ResetCond["ObjectList"]:

                self.ENTITY_CLIENT.spawn_REQUEST("OBJECT", x)
                while rclpy.ok():
                    rclpy.spin_once(self.ENTITY_CLIENT)
                    if self.ENTITY_CLIENT.future_SPAWN.done():
                        try:
                            spawnRES = self.ENTITY_CLIENT.future_SPAWN.result()
                        except Exception as exc:
                            self.ENTITY_CLIENT.get_logger().info("[R3M Cell] - /SpawnEntity ROS2 Service call failed. ERROR: " + str(exc))
                            return(False)
                        else:
                            self.ENTITY_CLIENT.get_logger().info("[R3M Cell] - /SpawnEntity RESULT: " + str(spawnRES.status_message))
                        break
    
        return(True)

# ========================================================================================= #
# ServiceClient (SPAWN/DELETE ROBOT + OBJECT):

class EntityClient(Node):

    def __init__(self):

        # Initialise ROS2 Node:
        super().__init__('r3m_EntityClient')

        # Create ROS2 Service Clients:
        self.cli_SPAWN = self.create_client(SpawnEntity, "/spawn_entity")  
        self.cli_DELETE = self.create_client(DeleteEntity, "/delete_entity") 

        # Declare REQUEST variable (of CUSTOM DATA type):
        self.req_SPAWN = SpawnEntity.Request()  
        self.req_DELETE = DeleteEntity.Request()

    def spawn_REQUEST(self, ELEMENT, INFORMATION):
        
        # ELEMENT can be: "ROBOT"/ "OBJECT"

        # INFORMATION:
        # Robot -> {Model - Link - EEType - Package - InitialPose - HomePose}
        # Object -> {Name - Link - CADFile - Package - InitialPose - CurrentPose - PreviousPose}
        
        # 1. SPAWN ROBOT:

        if ELEMENT == "ROBOT":
        
            # LOAD URDF of ROBOT:
            urdf_file_path = os.path.join(get_package_share_directory(INFORMATION["Package"]), 'urdf', INFORMATION["Model"] + '.urdf.xacro')
            xacro_file = xacro.process_file(urdf_file_path, mappings={"name": INFORMATION["Model"]})
            
            # ARGUMENTS:
            self.req_SPAWN.name = INFORMATION["Model"]
            self.req_SPAWN.xml = xacro_file.toxml()
            self.req_SPAWN.initial_pose.position.x = INFORMATION["InitialPose"]["x"]
            self.req_SPAWN.initial_pose.position.y = INFORMATION["InitialPose"]["y"]
            self.req_SPAWN.initial_pose.position.z = INFORMATION["InitialPose"]["z"]
            self.req_SPAWN.initial_pose.orientation.x = INFORMATION["InitialPose"]["qx"]
            self.req_SPAWN.initial_pose.orientation.y = INFORMATION["InitialPose"]["qy"]
            self.req_SPAWN.initial_pose.orientation.z = INFORMATION["InitialPose"]["qz"]
            self.req_SPAWN.initial_pose.orientation.w = INFORMATION["InitialPose"]["qw"]

            # Assign RESULT value (future):
            self.future_SPAWN = self.cli_SPAWN.call_async(self.req_SPAWN)

        ## 2. SPAWN CUBE:

        elif ELEMENT == "OBJECT":

            # LOAD URDF of CUBE:
            urdf_file_path = os.path.join(get_package_share_directory(INFORMATION["Package"]), 'urdf', 'objects', INFORMATION["CADFile"] + '.urdf')
            xacro_file = xacro.process_file(urdf_file_path, mappings={"name": INFORMATION["Name"]})
            
            IP = {}

            # Check if RANDOM values are needed:
            for key, value in INFORMATION["InitialPose"].items():
                
                if isinstance(value, str):
                    LIM = ast.literal_eval(value)
                    VAL = round(random.uniform(LIM["min"],LIM["max"]), 2)
                    
                    IP[key] = VAL
                    
                else: 
                    IP[key] = INFORMATION["InitialPose"][key]

            # ARGUMENTS:
            self.req_SPAWN.name = INFORMATION["Name"]
            self.req_SPAWN.xml = xacro_file.toxml()
            self.req_SPAWN.initial_pose.position.x = IP["x"]
            self.req_SPAWN.initial_pose.position.y = IP["y"]
            self.req_SPAWN.initial_pose.position.z = IP["z"]
            self.req_SPAWN.initial_pose.orientation.x = IP["qx"]
            self.req_SPAWN.initial_pose.orientation.y = IP["qy"]
            self.req_SPAWN.initial_pose.orientation.z = IP["qz"]
            self.req_SPAWN.initial_pose.orientation.w = IP["qw"]

            # Assign RESULT value (future):
            self.future_SPAWN = self.cli_SPAWN.call_async(self.req_SPAWN)

    def delete_REQUEST(self, ELEMENT, INFORMATION):

        ## 1. DELETE ROBOT:
        if ELEMENT == "ROBOT":
            self.req_DELETE.name = INFORMATION["Model"]
            self.future_DELETE = self.cli_DELETE.call_async(self.req_DELETE)
        
        ## 2. DELETE OBJECT:
        elif ELEMENT == "OBJECT":
            self.req_DELETE.name = INFORMATION["Name"]
            self.future_DELETE = self.cli_DELETE.call_async(self.req_DELETE)


# ========================================================================================= #
# ================================== RESET for TRAINING =================================== #
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

    PKG_ = PKG.replace("_gazebo", "")
    CMD = "gnome-terminal -- ros2 launch ros2srrc_launch moveit2.launch.py package:=" + PKG_ + " config:=" + CNF
    
    PROCESS = subprocess.Popen(CMD, shell=True)
    GzLAUNCH_COMPLETE = False

    T = time.time()

    while (time.time() < T + 30.0):
        rclpy.spin_once(SUBNode)
        if GzLAUNCH_COMPLETE:
            SUBNode.destroy_node()
            del SUBNode
            return(True)

    SUBNode.destroy_node()
    del SUBNode
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

    GAZEBO_close()
    time.sleep(10.0)
    RES = GAZEBO_start(PKG, CNF)
    
    return(RES)