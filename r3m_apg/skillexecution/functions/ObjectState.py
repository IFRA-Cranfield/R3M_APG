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
from objectpose_msgs.msg import ObjectPose

# ========================================================================================= #
# =================================== CLASSES/FUNCTIONS =================================== #
# ========================================================================================= #

# ========================================================================================= #
# OBJECT CLASS:
class OBJECT(Node):

    def __init__(self, ObjectList, R3MPerception=False):
        
        self.R3MP = R3MPerception
        
        self.CurrentPose = []
        self.PreviousPose = []
        self.ObjectList = ObjectList

        self.DET =[]
                
        # "ObjectList": [{Name - Link - CADFile - Package - InitialPose - CurrentPose - PreviousPose}, ..]

        super().__init__("r3m_ObjectPose_Subscriber")
        self.SUBList = []
        
        for x in ObjectList:
            
            if self.R3MP:
                TopicName = "/" + x["Name"] + "/ObjectPoseEstimation"
            else:
                TopicName = "/" + x["Name"] + "/ObjectPose"
            
            self.SUBList.append(self.create_subscription(ObjectPose, TopicName, self.CALLBACK_FN, 10))
            
            EmptyPose = ObjectPose()
            EmptyPose.objectname = x["Name"]
            EmptyPose.x = 0.0
            EmptyPose.y = 0.0
            EmptyPose.z = 0.0
            EmptyPose.qx = 0.0
            EmptyPose.qy = 0.0
            EmptyPose.qz = 0.0
            EmptyPose.qw = 0.0
            
            x["CurrentPose"] = EmptyPose
            x["PreviousPose"] = EmptyPose

            # Initialise self.DET:
            self.DET.append({"Name": x["Name"], "Detected": False})

    def CALLBACK_FN(self, OBJ):

        # 1. Assign CURRENTPOSE to PREVIOUSPOSE:
        # 2. Assign NEWPOSE to CURRENTPOSE:

        # ASSIGN -> PreviousPose:
        for x in self.DET:
            if (x["Name"] == OBJ.objectname and x["Detected"] == False):

                x["Detected"] = True

                for y in self.ObjectList:
                    if (OBJ.objectname == y["Name"]):
                        
                        y["PreviousPose"] = y["CurrentPose"]
                        y["CurrentPose"] = OBJ

        # ASSIGN -> CurrentPose (just in case to take the last subscribed value):
        for x in self.DET:
            if (x["Name"] == OBJ.objectname and x["Detected"] == True):

                for y in self.ObjectList:
                    if (OBJ.objectname == y["Name"]):
                        
                        y["CurrentPose"] = OBJ

    def ResetObjectList(self):

        for x in self.ObjectList:
            
            EmptyPose = ObjectPose()
            EmptyPose.objectname = x["Name"]
            EmptyPose.x = 0.0
            EmptyPose.y = 0.0
            EmptyPose.z = 0.0
            EmptyPose.qx = 0.0
            EmptyPose.qy = 0.0
            EmptyPose.qz = 0.0
            EmptyPose.qw = 0.0
            
            x["CurrentPose"] = EmptyPose
            x["PreviousPose"] = EmptyPose
            
        for x in self.DET:
            x["Detected"] = False
        
    def GetObjectPose(self):
        
        if self.R3MP:
            Td = 2.0
        else:
            Td = 0.25
        
        # 1. Spin node:
        T = time.time() + Td
        while time.time() < T:
            rclpy.spin_once(self, timeout_sec=1.0)

        # 2. Reset self.DET:
        for x in self.DET:
            x["Detected"] = False
        
        # 3. RETURN:
        return(self.ObjectList)
    
    def CheckObjectPose(self):
        
        SUBDetected = False
        while SUBDetected == False:
            
            SUBDetected = True
            rclpy.spin_once(self)
            
            for x in self.DET:
                if x["Detected"] == False:
                    SUBDetected = False
                    
        return()