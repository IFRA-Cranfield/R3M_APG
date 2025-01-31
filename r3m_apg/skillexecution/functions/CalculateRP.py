#!/usr/bin/python3

# # # # # # # # # # # # # # # # # #                                  
#                                 #
#   ===== COPYRIGHT HERE =====    #
#                                 #
# # # # # # # # # # # # # # # # # #

# ========================================================================================= #
# ======================================== INCLUDE ======================================== #
# ========================================================================================= #

# CUSTOM ROS2 MSG/SRV/ACTION:
from ros2srrc_data.msg import Robpose

def CALCULATE_RobPose(POSE, ObjectList):
    
    # Initialise -> RESULT:
    RESULT = {}
    
    # Initialise -> GOAL POSE:
    GoalPose = Robpose()

    # COMPUTE -> POSITION:
    if POSE["position"]["type"] == "DYNAMIC":

        objFOUND_P = False
        for OBJ in ObjectList:

            TopicName = "/" + OBJ["Name"] + "/ObjectPose"
            if POSE["position"]["topic"] == TopicName:

                GoalPose.x = OBJ["CurrentPose"].x + POSE["position"]["transform"].x
                GoalPose.y = OBJ["CurrentPose"].y + POSE["position"]["transform"].y
                GoalPose.z = OBJ["CurrentPose"].z + POSE["position"]["transform"].z
                
                objFOUND_P = True
                break
    
        if objFOUND_P == False:

            RESULT["Message"] = "Tried to compute POSITION from " +  POSE["position"]["topic"] + "ROS 2 Topic but topic was not found."
            RESULT["Success"] = False
            RESULT["ExecTime"] = -1.0

            return(RESULT)

    else:

        GoalPose.x = POSE["position"]["pose"].x
        GoalPose.y = POSE["position"]["pose"].y
        GoalPose.z = POSE["position"]["pose"].z

    # COMPUTE -> ORIENTATION:
    if POSE["orientation"]["type"] == "DYNAMIC":

        objFOUND_O = False
        for OBJ in ObjectList:

            TopicName = "/" + OBJ["Name"] + "/ObjectPose"
            if POSE["orientation"]["topic"] == TopicName:

                GoalPose.qx = OBJ["CurrentPose"].qx + POSE["orientation"]["transform"].qx
                GoalPose.qy = OBJ["CurrentPose"].qy + POSE["orientation"]["transform"].qy
                GoalPose.qz = OBJ["CurrentPose"].qz + POSE["orientation"]["transform"].qz
                GoalPose.qw = OBJ["CurrentPose"].qw + POSE["orientation"]["transform"].qw

                objFOUND_O = True
                break

        if objFOUND_O == False:

            RESULT = {}
            RESULT["Message"] = "Tried to compute ORIENTATION from " +  POSE["orientation"]["topic"] + "ROS 2 Topic but topic was not found."
            RESULT["Success"] = False
            RESULT["ExecTime"] = -1.0

            return(RESULT)
    
    else:

        GoalPose.qx = POSE["orientation"]["pose"].qx
        GoalPose.qy = POSE["orientation"]["pose"].qy
        GoalPose.qz = POSE["orientation"]["pose"].qz
        GoalPose.qw = POSE["orientation"]["pose"].qw
        
    RESULT["Success"] = True
    RESULT["Pose"] = GoalPose
        
    return(RESULT)