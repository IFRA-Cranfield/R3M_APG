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
import sys, subprocess, time, os, psutil, yaml

# ROS2:
import rclpy
from rclpy.node import Node
from ament_index_python.packages import get_package_share_directory

# CUSTOM ROS2 MSG/SRV/ACTION:
from r3m_data.srv import SkillExecution
from r3m_perception_data.srv import OneShotDet

# Import CLASSES/Functions:
PATH_F = os.path.join(get_package_share_directory("r3m_apg"), 'skillexecution', 'functions')
sys.path.append(PATH_F)
from RestartGazebo import GAZEBO_start, GAZEBO_close

# ========================================================================================= #
# LAUNCH -> APG Node:   
def LaunchAPG(CONFIG, PERCEPTION):

    if PERCEPTION == False:
        CMD = "gnome-terminal -- ros2 run r3m_apg r3m_SkillExecution_Gazebo.py train:=False config:=" + CONFIG
    if PERCEPTION == "MarkerGrid":
        CMD = "gnome-terminal -- ros2 run r3m_apg r3m_SkillExecution_Gazebo.py train:=False perception:=True config:=" + CONFIG
    if PERCEPTION == "r3m":
        CMD = "gnome-terminal -- ros2 run r3m_apg r3m_SkillExecution_Gz_Perception.py config:=" + CONFIG
    
    print("[APG NODE LAUNCH]: Executing command -> " + CMD)
    
    PROCESS = subprocess.Popen(CMD, shell=True)
    
    NODE = rclpy.create_node('R3M_LaunchAPG_Node')
    cli = NODE.create_client(SkillExecution, "/r3m_SkillExecution")
    
    T = time.time()
    while (time.time() < T + 10.0):
        
        if cli.wait_for_service():
            
            cli.destroy()
            NODE.destroy_node()
        
            print("[APG NODE LAUNCH]: APG /r3m_SkillExecution ROS 2 service server successfully launched.")
            print("")
            return(True)

    cli.destroy()
    NODE.destroy_node()
    
    print("[APG NODE LAUNCH]: APG /r3m_SkillExecution ROS 2 service server launch ERROR.")
    print("")
    return(False)

# ========================================================================================= #
# LAUNCH -> OSD+M6D Nodes: 
def LaunchR3MPerception():
    
    CMD1 = "gnome-terminal -- ros2 run r3m_perception OSD_server.py"
    print("[R3M Perception -OSD- NODE LAUNCH]: Executing command -> " + CMD1)
    PROCESS1 = subprocess.Popen(CMD1, shell=True)
    
    CMD2 = "gnome-terminal -- ros2 run r3m_perception M6D_server.py"
    print("[R3M Perception -M6D- NODE LAUNCH]: Executing command -> " + CMD2)
    PROCESS2 = subprocess.Popen(CMD2, shell=True)
    
    NODE = rclpy.create_node('R3M_LaunchR3MP_Node')
    cli = NODE.create_client(OneShotDet, "/R3MPerception_OSD")
    
    T = time.time()
    while (time.time() < T + 300.0):
        
        if cli.wait_for_service():
            
            cli.destroy()
            NODE.destroy_node()
        
            print("[R3M Perception LAUNCH]: One-Shot Detection and Megapose6D ROS 2 Service Servers successfully launched.")
            print("")
            return(True)
        
    print("[R3M Perception LAUNCH] - ERROR: One-Shot Detection and Megapose6D ROS 2 Service Servers not launched.")
    return(False)

# ========================================================================================= #           
# get CONFIG:
def getCNF(CONFIG):

    PATH = os.path.join(get_package_share_directory('r3m_apg'), 'apg', 'usecase')
    YAML_PATH = PATH + "/" + CONFIG + ".yaml"

    with open(YAML_PATH, 'r') as YAML:
        icYAML = yaml.safe_load(YAML)

    CNF = icYAML["Information"]["Name"]

    return(CNF)

# ========================================================================================= #
# LAUNCH -> PERCEPTION-MG Node: 
def LaunchMGPerception(MODEL, PKG, CNF):

    if "r3mcell_cu" in PKG:
        if "_1" in CNF:
            CELL = "irb120-cranfield"
        else:
            CELL = "ur3-cranfield"
    
    else:
        if "_1" in CNF:
            CELL = "irb1200-amrc"
        else:
            CELL = "irb6640-amrc"

    CMD = "gnome-terminal -- ros2 run r3m_ope PositionEstimation_MarkerGrid.py environment:=gazebo model:=" + MODEL + " cell:=" + CELL + " visualize:=True"
    print("[R3M Perception -MarkerGrid- NODE LAUNCH]: Executing command -> " + CMD)
    PROCESS = subprocess.Popen(CMD, shell=True)
            
# ========================================================================================= #           
# EVALUATE INPUT ARGUMENTS:
def AssignArgument(ARGUMENT):
    ARGUMENTS = sys.argv
    for y in ARGUMENTS:
        if (ARGUMENT + ":=") in y:
            ARG = y.replace((ARGUMENT + ":="),"")
            return(ARG)

# ========================================================================================= #
# ========================================= MAIN ========================================== #
# ========================================================================================= #
def main(args=None):
    
    rclpy.init(args=args)
    
    # === PARAMETERS === #
    # Get ROS2 Parameter value -> package:
    PACKAGE = AssignArgument("package")
    if PACKAGE != None:
        None
    else:
        print("")
        print("ERROR: package INPUT ARGUMENT has not been defined. Please try again.")
        print("Closing... BYE!")
        exit()
    # Get ROS2 Parameter value -> config:
    CONFIG = AssignArgument("config")
    if CONFIG != None:
        None
    else:
        print("")
        print("ERROR: config INPUT ARGUMENT has not been defined. Please try again.")
        print("Closing... BYE!")
        exit()
    # Get ROS2 Parameter value -> perception:
    PERCEPTION = AssignArgument("perception")
    if PERCEPTION == "r3m" or PERCEPTION == "MarkerGrid":
        None
    elif PERCEPTION == None:
        PERCEPTION = False
    else:
        print("")
        print("ERROR: perception INPUT ARGUMENT has not been correctly defined. Please try again.")
        print("Closing... BYE!")
        exit()

    try:
        
        CNF = getCNF(CONFIG)
        
        # 1. LAUNCH GAZEBO ENVIRONMENT:
        RES1 = GAZEBO_start(PACKAGE,CONFIG)
        if RES1 == False:
            print("")
            print("ERROR: Gazebo Environment START failed.")
            print("Closing... BYE!")
            exit()
        0
        # 2. LAUNCH PERCEPTION:
        if PERCEPTION == "r3m":
            
            RES2 = LaunchR3MPerception()
            if RES2 == False:
                print("")
                print("ERROR: R3M Perception (OSD+M6D Nodes) START failed.")
                print("Closing... BYE!")
                exit()
        
        elif PERCEPTION == "MarkerGrid":
            MODEL = AssignArgument("model")
            if MODEL == None:
                print("")
                print("ERROR: model INPUT ARGUMENT has not been correctly defined. Please try again.")
                print("Closing... BYE!")
                exit()
            else:
                LaunchMGPerception(MODEL, PACKAGE, CONFIG)
            
        # 3. LAUNCH R3M-APG ENVIRONMENT:
        RES3 = LaunchAPG(CONFIG,PERCEPTION)
        if RES3 == False:
            print("")
            print("ERROR: APG Node START failed.")
            print("Closing... BYE!")
            exit()
        
        # Infinite LOOP -> WAIT FOR KEYBOARD INTERRUPT:
        print("[R3M Cell - EXECUTION] - GAZEBO + R3M-APG ENVIRONMENT ready.")
        print("[R3M Cell - EXECUTION] - PRESS CTRL+C to CLOSE GAZEBO and the R3M-APG ENVIRONMENT.")
        while True:
            None
        
    except KeyboardInterrupt:
        
        print("[R3M Cell - EXECUTION] - Shutting down due to keyboard interrupt.")
        
        # Close Gazebo environment:
        GAZEBO_close()
        
        # Close ROS 2 Nodes:
        os.system("pkill -f r3m_SkillExecution_Gazebo.py")  
        os.system("pkill -f r3m_SkillExecution_Gz_Perception.py") 
        os.system("pkill -f PositionEstimation_MarkerGrid.py")  
        os.system("pkill -f OSD_server.py")  
        os.system("pkill -f M6D_server.py")  
        
    finally:
        rclpy.shutdown()
    
if __name__ == '__main__':
    main()