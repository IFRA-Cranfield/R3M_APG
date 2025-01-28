#!/usr/bin/python3

import os, yaml
from objectpose_msgs.msg import ObjectPose
from ament_index_python.packages import get_package_share_directory

# ===== CONVERT FROM SLOT NUMBER TO POSE ===== #
def GetPose(BATTERIES, CELL):

    POSES = []
    
    for i, BT in enumerate(BATTERIES):

        POSE = ObjectPose()
        POSE.objectname = "Battery" + str(i+1)
        POSE.x, POSE.y, POSE.z, POSE.qx, POSE.qy, POSE.qz, POSE.qw = getPOSEfromYAML(BT,CELL)
        POSES.append(POSE)

    return(POSES)

def getPOSEfromYAML(BT,CELL):

    if BT == 0:
        return(0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0)
    
    else:

        PATH = os.path.join(get_package_share_directory('r3m_apg'), 'apg', 'usecase')
        
        if CELL == "AMRC":
            YAML_PATH = PATH + "/r3mcell_amrc_24.yaml"
        else:
            YAML_PATH = PATH + "/r3mcell_cu_15.yaml"

        with open(YAML_PATH, 'r') as YAML:
            icYAML = yaml.safe_load(YAML)

        x = icYAML["BatteryLocation"][str(BT)]["x"]
        y = icYAML["BatteryLocation"][str(BT)]["y"]
        z = icYAML["BatteryLocation"][str(BT)]["z"]
        qx = icYAML["BatteryLocation"][str(BT)]["qx"]
        qy = icYAML["BatteryLocation"][str(BT)]["qy"]
        qz = icYAML["BatteryLocation"][str(BT)]["qz"]
        qw = icYAML["BatteryLocation"][str(BT)]["qw"]

        return(x, y, z, qx, qy, qz, qw)

# ===== CALCULATE BATTERY LOCATION SLOT ===== #
def GetSlot(X,Y,CELL):
    
    if CELL == "AMRC":
        
        if (-1 <= X <= 9) and (102 <= Y <= 112):
            return(1)
        elif (-1 <= X <= 9) and (87 <= Y <= 97):
            return(2)
        elif (-1 <= X <= 9) and (71 <= Y <= 81):
            return(3)
        elif (-1 <= X <= 9) and (56 <= Y <= 66):
            return(4)
        elif (-1 <= X <= 9) and (41 <= Y <= 51):
            return(5)
        elif (-1 <= X <= 9) and (27 <= Y <= 37):
            return(6)
        elif (-1 <= X <= 9) and (12 <= Y <= 22):
            return(7)
        elif (-1 <= X <= 9) and (0 <= Y <= 10):
            return(8)
        elif (-1 <= X <= 9) and (-14 <= Y <= -4):
            return(9)

        elif (12 <= X <= 22) and (94 <= Y <= 104):
            return(10)
        elif (12 <= X <= 22) and (77 <= Y <= 87):
            return(11)
        elif (12 <= X <= 22) and (62 <= Y <= 72):
            return(12)
        elif (12 <= X <= 22) and (47 <= Y <= 57):
            return(13)
        elif (12 <= X <= 22) and (33 <= Y <= 43):
            return(14)
        elif (12 <= X <= 22) and (20 <= Y <= 30):
            return(15)
        elif (12 <= X <= 22) and (7 <= Y <= 17):
            return(16)
        elif (12 <= X <= 22) and (-5 <= Y <= 5):
            return(17)
        elif (12 <= X <= 22) and (-19 <= Y <= -9):
            return(18)

        elif (26 <= X <= 36) and (102 <= Y <= 112):
            return(19)
        elif (26 <= X <= 36) and (87 <= Y <= 97):
            return(20)
        elif (26 <= X <= 36) and (71 <= Y <= 81):
            return(21)
        elif (26 <= X <= 36) and (56 <= Y <= 66):
            return(22)
        elif (26 <= X <= 36) and (41 <= Y <= 51):
            return(23)
        elif (26 <= X <= 36) and (27 <= Y <= 37):
            return(24)
        elif (26 <= X <= 36) and (12 <= Y <= 22):
            return(25)
        elif (26 <= X <= 36) and (0 <= Y <= 10):
            return(26)
        elif (26 <= X <= 36) and (-14 <= Y <= -4):
            return(27)

        elif (35 <= X <= 45) and (94 <= Y <= 104):
            return(28)
        elif (35 <= X <= 45) and (77 <= Y <= 87):
            return(29)
        elif (35 <= X <= 45) and (62 <= Y <= 72):
            return(30)
        elif (35 <= X <= 45) and (47 <= Y <= 57):
            return(31)
        elif (35 <= X <= 45) and (33 <= Y <= 43):
            return(32)
        elif (35 <= X <= 45) and (20 <= Y <= 30):
            return(33)
        elif (35 <= X <= 45) and (7 <= Y <= 17):
            return(34)
        elif (35 <= X <= 45) and (-5 <= Y <= 5):
            return(35)
        elif (35 <= X <= 45) and (-19 <= Y <= -9):
            return(36)

        else:
            return(0)

    else:
        return(0)