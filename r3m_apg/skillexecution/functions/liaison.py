#!/usr/bin/python3

# # # # # # # # # # # # # # # # # #                                  
#                                 #
#   ===== COPYRIGHT HERE =====    #
#                                 #
# # # # # # # # # # # # # # # # # #

# ========================================================================================= #
# ======================================== INCLUDE ======================================== #
# ========================================================================================= #

# Import system functions:
import math

# CUSTOM ROS2 MSG/SRV/ACTION:
from r3m_data.msg import Liaison
from r3m_data.msg import Pose

# ========================================================================================= #
# =================================== CLASSES/FUNCTIONS =================================== #
# ========================================================================================= #

# ========================================================================================= #
# Vacuum Gripper:
class LiaisonCheck():

    def __init__(self, LiaisonList):

        # Initialise CLASSES to be used:
        self.LiaisonList = LiaisonList
        self.LiaisonVECTOR = []

        # Initialise VECTOR:
        for x in LiaisonList:

            self.LiaisonRESULT = Liaison()
            
            self.LiaisonRESULT.name = x["Name"]
            self.LiaisonRESULT.parent = x["Parent"]
            self.LiaisonRESULT.child = x["Child"]

            if x["Transform"]["position"]:
                self.LiaisonRESULT.transform.position = True
                self.LiaisonRESULT.transform.pose.x = x["Transform"]["x"]
                self.LiaisonRESULT.transform.pose.y = x["Transform"]["y"]
                self.LiaisonRESULT.transform.pose.z = x["Transform"]["z"]
            else:
                self.LiaisonRESULT.transform.position = False
            
            if x["Transform"]["orientation"]:
                self.LiaisonRESULT.transform.orientation = True
                self.LiaisonRESULT.transform.pose.qx = x["Transform"]["qx"]
                self.LiaisonRESULT.transform.pose.qy = x["Transform"]["qy"]
                self.LiaisonRESULT.transform.pose.qz = x["Transform"]["qz"]
                self.LiaisonRESULT.transform.pose.qw = x["Transform"]["qw"]
            else:
                self.LiaisonRESULT.transform.orientation = False
                
            self.LiaisonRESULT.diff_max = x["Transform"]["diffMax"]
            self.LiaisonRESULT.liaison_met = 0 

            self.LiaisonVECTOR.append(self.LiaisonRESULT) 

    def CHECK(self, ObjectList):

        # Flag to check if ALL LIAISONS are met:
        allMET = True

        for x in self.LiaisonVECTOR:

            # Get OBJECT POSE for -> PARENT:
            if x.parent == "GLOBAL":
                x.parentpose = Pose()
            else:

                for y in ObjectList:
                    if y["Name"] == x.parent:

                        x.parentpose = Pose()
                        x.parentpose.x = y["CurrentPose"].x
                        x.parentpose.y = y["CurrentPose"].y
                        x.parentpose.z = y["CurrentPose"].z
                        x.parentpose.qx = y["CurrentPose"].qx
                        x.parentpose.qy = y["CurrentPose"].qy
                        x.parentpose.qz = y["CurrentPose"].qz
                        x.parentpose.qw = y["CurrentPose"].qw

            # Get OBJECT POSE for -> CHILD:
            for y in ObjectList:
                if y["Name"] == x.child:

                    x.childpose = Pose()
                    x.childpose.x = y["CurrentPose"].x
                    x.childpose.y = y["CurrentPose"].y
                    x.childpose.z = y["CurrentPose"].z
                    x.childpose.qx = y["CurrentPose"].qx
                    x.childpose.qy = y["CurrentPose"].qy
                    x.childpose.qz = y["CurrentPose"].qz
                    x.childpose.qw = y["CurrentPose"].qw

            # CALCULATE -> GOAL POSE for CHILD:
            x.childpose_goal = self.calculateGOAL(x.childpose, x.parentpose, x.transform)

            # CALCULATE -> DIFF:
            x.diff = self.calculateDIFF(x.childpose, x.childpose_goal, x.transform)

            # CHECK if -> LIAISON IS MET:
            if x.diff < x.diff_max:
                x.liaison_met = 1
            else:
                x.liaison_met = 0
                allMET = False

        RES = {}
        RES["LiaisonVector"] = self.LiaisonVECTOR
        RES["allMET"] = allMET

        return(RES)
    
    def calculateGOAL(self, poseCHILD, posePARENT, TR):

        # INITIALISE -> Goal Pose:
        GOAL = Pose()

        # Calculate GOAL POSITION:
        if TR.position:
            GOAL.x = posePARENT.x + TR.pose.x
            GOAL.y = posePARENT.y + TR.pose.y
            GOAL.z = posePARENT.z + TR.pose.z
        else:
            GOAL.x = poseCHILD.x
            GOAL.y = poseCHILD.y 
            GOAL.z = poseCHILD.z

        # Calculate GOAL ORIENTATION:
        if TR.orientation:
            goalOR = Pose()
            (GOAL.qx, GOAL.qy, GOAL.qz, GOAL.qw) = self.multiplyQUAT(posePARENT, TR.pose)
        else:
            GOAL.qx = poseCHILD.qx
            GOAL.qy = poseCHILD.qy 
            GOAL.qz = poseCHILD.qz
            GOAL.qw = poseCHILD.qw

        # RETURN GOAL:
        return(GOAL)
    
    def calculateDIFF(self, poseCHILD, poseGOAL, TR):

        # POSITION ERROR: Norm of the (p1-p0) difference vector:

        DIFx = abs(poseCHILD.x - poseGOAL.x)
        DIFy = abs(poseCHILD.y - poseGOAL.y)
        DIFz = abs(poseCHILD.z - poseGOAL.z)

        ERROR_POS = math.sqrt(DIFx*DIFx + DIFy*DIFy + DIFz*DIFz)

        # ROTATION ERROR: Norm of the (C = A*inv(B)) difference quaternion:

        Ax = poseCHILD.qx
        Ay = poseCHILD.qy
        Az = poseCHILD.qz
        Aw = poseCHILD.qw

        Bx = -poseGOAL.qx
        By = -poseGOAL.qy
        Bz = -poseGOAL.qz
        Bw = poseGOAL.qw

        qw = Aw*Bw - Ax*Bx - Ay*By - Az*Bz # Not needed.
        qx = Aw*Bx + Ax*Bw + Ay*Bz - Az*By
        qy = Aw*By - Ax*Bz + Ay*Bw + Az*Bx
        qz = Aw*Bz + Ax*By - Ay*Bx + Az*Bw

        ERROR_ROT = math.sqrt((qx*qx)+(qy*qy)+(qz*qz))

        # ASSIGN ERROR VALUE, and RETURN:
        if TR.position == True and TR.orientation == True:
            ERROR = (ERROR_POS + ERROR_ROT)/2
        elif TR.position == True and TR.orientation == False:
            ERROR = ERROR_POS 
        else:
            ERROR = ERROR_ROT

        return(ERROR)
    
    def multiplyQUAT(self, A, B):

        qx = A.qw*B.qx + A.qx*B.qw + A.qy*B.qz - A.qz*B.qy
        qy = A.qw*B.qy - A.qx*B.qz + A.qy*B.qw + A.qz*B.qx
        qz = A.qw*B.qz + A.qx*B.qy - A.qy*B.qx + A.qz*B.qw
        qw = A.qw*B.qw - A.qx*B.qx - A.qy*B.qy - A.zq*B.qz

        return(qx,qy,qz,qw)