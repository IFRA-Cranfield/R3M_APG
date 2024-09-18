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
import sys, subprocess, time, os

# ROS2:
import rclpy
from rclpy.node import Node
from ament_index_python.packages import get_package_share_directory
from rclpy.executors import MultiThreadedExecutor

# CUSTOM ROS2 MSG/SRV/ACTION:
from std_srvs.srv import Empty
from r3m_data.srv import SkillExecution

# Import CLASSES/Functions:
PATH_F = os.path.join(get_package_share_directory("r3m_apg"), 'skillexecution', 'functions')
sys.path.append(PATH_F)
from RestartGazebo import GAZEBO_start, GAZEBO_close

# ========================================================================================= #
# =================================== CLASSES/FUNCTIONS =================================== #
# ========================================================================================= #

# ========================================================================================= #
# RESET TRAINING EMVIRONMENT -> ROS 2 Service Server:
class TrainingENVReset(Node):
    
    def __init__(self, PACKAGE, CONFIG):

        # Initialise SERVICE SERVER:
        super().__init__('r3m_ResetTraining_Node')                                              
        self.srv = self.create_service(Empty, "/r3m_ResetTraining", self.ResetEnvironment)
        
        # Execute -> Gazebo ENVIRONMENT:
        RES1 = GAZEBO_start(PACKAGE,CONFIG)
        if RES1 == False:
            print("")
            print("ERROR: Gazebo Environment START failed.")
            print("Closing... BYE!")
            exit()
        
        # Execute -> APG Node:
        RES2 = self.LaunchAPG(CONFIG)
        if RES2 == False:
            print("")
            print("ERROR: APG Node START failed.")
            print("Closing... BYE!")
            exit()
            
        self.PACKAGE = PACKAGE
        self.CONFIG = CONFIG
        
    def ResetEnvironment(self, request, response):
        
        # 1. CLOSE -> Gazebo and APG windows:
        print("")
        print("[RESET ENVIRONMENT]: TRAINING ENVIRONMENT RESET requested.")
        print("[RESET ENVIRONMENT]: Closing Gazebo and APG windows...")
        
        GAZEBO_close()
        self.APG_close()
        
        time.sleep(1.0)
        print("[RESET ENVIRONMENT]: Windows closed!")
        
        # Execute -> Gazebo ENVIRONMENT:
        print("[RESET ENVIRONMENT]: Re-Starting GAZEBO ENVIRONMENT...")
        RES1 = GAZEBO_start(self.PACKAGE,self.CONFIG)
        if RES1 == False:
            print("")
            print("ERROR: Gazebo Environment START failed.")
            print("Closing... BYE!")
            exit()
        print("[RESET ENVIRONMENT]: SUCCESSFUL.")
        
        # Execute -> APG Node:
        print("[RESET ENVIRONMENT]: Re-Starting APG NODE...")
        RES2 = self.LaunchAPG(self.CONFIG)
        if RES2 == False:
            print("")
            print("ERROR: APG Node START failed.")
            print("Closing... BYE!")
            exit()
        print("[RESET ENVIRONMENT]: SUCCESSFUL.")
            
        return(response)
        
    def LaunchAPG(self, CONFIG):

        CMD = "gnome-terminal -- ros2 run r3m_apg r3m_SkillExecution_Gazebo.py config:=" + CONFIG
        
        print("[APG NODE LAUNCH]: Executing command -> " + CMD)
        
        PROCESS = subprocess.Popen(CMD, shell=True)
        self.cli = self.create_client(SkillExecution, "/r3m_SkillExecution")
        
        T = time.time()
        while (time.time() < T + 10.0):
            
            if self.cli.wait_for_service():
                
                self.cli.destroy()
                del self.cli
            
                print("[APG NODE LAUNCH]: APG /r3m_SkillExecution ROS 2 service server successfully launched.")
                print("")
                return(True)

        self.cli.destroy()
        del self.cli
        
        print("[APG NODE LAUNCH]: APG /r3m_SkillExecution ROS 2 service server launch ERROR.")
        print("")
        return(False)
    
    def RestartAPG(self, CONFIG):
        
        print("")
        print("[APG RE-START]: Re-start of APG node requested.")

        print("[APG RE-START]: Closing current APG window...")
        self.APG_close()
        print("[APG RE-START]: APG window closed.")
        
        time.sleep(5.0)
        
        print("[APG RE-START]: Starting a new APG-Node environment...")
        RES = self.LaunchAPG(CONFIG)
        
        return(RES)
    
    def APG_close(self):
        os.system("pkill -f r3m_SkillExecution_Gazebo.py")  
            
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

    # Multi-Threaded EXECUTOR:
    EXECUTOR = MultiThreadedExecutor()

    # Initialise NODE:
    r3mNode = TrainingENVReset(PACKAGE,CONFIG)
    r3mNode.get_logger().info("[R3M Cell - TRAINING] - /r3m_ResetTraining ROS2 Service Server running, ROS2 node generated.")
    
    EXECUTOR.add_node(r3mNode)

    try:
        EXECUTOR.spin()
    except KeyboardInterrupt:
        r3mNode.get_logger().info("[R3M Cell - TRAINING] - Shutting down due to keyboard interrupt.")
        r3mNode.APG_close()
        GAZEBO_close()
    finally:
        r3mNode.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()