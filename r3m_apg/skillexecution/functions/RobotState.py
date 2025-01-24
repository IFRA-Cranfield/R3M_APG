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
import time

# ROS2:
import rclpy
from rclpy.node import Node

# CUSTOM ROS2 MSG/SRV/ACTION:
from ros2srrc_data.msg import Robpose
from r3m_data.msg import Pose

# ========================================================================================= #
# =================================== CLASSES/FUNCTIONS =================================== #
# ========================================================================================= #

# ========================================================================================= #
# RobState:
class ROB_STATE(Node):

    def __init__(self):

        super().__init__("r3m_RobotPose_Subscriber")
        self.create_subscription(Robpose, "Robpose", self.CALLBACK_FN, 10)
        
        self.POSE = Pose()
            
    def CALLBACK_FN(self, POSE):

        self.POSE.x = POSE.x
        self.POSE.y = POSE.y
        self.POSE.z = POSE.z
        
        self.POSE.qx = POSE.qx
        self.POSE.qy = POSE.qy
        self.POSE.qz = POSE.qz
        self.POSE.qw = POSE.qw
        
    def GetRobotPose(self):
        
        Td = 0.25
        
        # 1. Spin node:
        T = time.time() + Td
        while time.time() < T:
            rclpy.spin_once(self, timeout_sec=1.0)
        
        # 2. RETURN:
        return(self.POSE)