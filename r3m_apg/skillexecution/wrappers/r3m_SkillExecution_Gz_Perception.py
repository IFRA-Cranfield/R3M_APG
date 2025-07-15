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
import os, sys, time, yaml, subprocess, random

# ROS2:
import rclpy
from rclpy.node import Node
from ament_index_python.packages import get_package_share_directory
from rclpy.executors import MultiThreadedExecutor

# CUSTOM ROS2 MSG/SRV/ACTION:
from std_srvs.srv import Empty
from r3m_data.srv import SkillExecution
from r3m_data.msg import Product
from r3m_data.msg import Pose

# Import -> CalculateRP function:
from CalculateRP import CALCULATE_RobPose

# IMPORT Python classes:
PATH = os.path.join(get_package_share_directory("ros2srrc_execution"), 'python')
PATH_robot = PATH + "/robot"
PATH_endeffector = PATH + "/endeffector"
PATH_endeffector_gz = PATH + "/endeffector_gz"
# ROBOT CLASS:
sys.path.append(PATH_robot)
from robot import RBT
# END EFFECTOR CLASSES (Gazebo):
sys.path.append(PATH_endeffector)
from robotiq_ur import RobotiqGRIPPER
from schunk_abb import SchunkGRIPPER
# END EFFECTOR CLASSES (Gazebo):
sys.path.append(PATH_endeffector_gz)
from parallelGripper import parallelGR
from vacuumGripper import vacuumGR

# Import CLASSES/Functions:
PATH_F = os.path.join(get_package_share_directory("r3m_apg"), 'skillexecution', 'functions')
sys.path.append(PATH_F)
from ObjectState import OBJECT
from ResetGazebo import GzRESET
from liaison import LiaisonCheck
from RobotState import ROB_STATE

from perception import R3MPerceptionClient

# Global VAR: 
EEState = 1
RobStep = 0
ProdStep = []

# ========================================================================================= #
# ================================ ROS2 - INPUT PARAMETERS ================================ #
# ========================================================================================= #

def GetIC_YAML(NAME):

    global ProdStep

    RESULT = {"UseCaseInfo": None, "Robot": None, "ObjectList": None, "Liaison": None, "Success": True}
    
    PATH = os.path.join(get_package_share_directory('r3m_apg'), 'apg', 'usecase')
    YAML_PATH = PATH + "/" + NAME + ".yaml"
    
    if not os.path.exists(YAML_PATH):
        RESULT["Success"] = False
        return (RESULT)

    # Get VALUES:
    with open(YAML_PATH, 'r') as YAML:
        icYAML = yaml.safe_load(YAML)
    
    RESULT["UseCaseInfo"] = icYAML["Information"]
    RESULT["Robot"] = icYAML["Robot"]
    
    # ===== OBJECT LIST ===== #
    RESULT["ObjectList"] = icYAML["ObjectList"]

    # Check for RANDOM EXTRA objects -> This is for the objects that can or cannot be spawned (random):
    if "ObjectExtra" in icYAML:

        OLextra = []
        li = []
        
        for x in icYAML["ObjectExtra"]:
            if random.choice([True,False]):
                OLextra.append(x)
                li.append(x["Name"])

        if len(OLextra) > 0:

            if RESULT["ObjectList"] != None:
                RESULT["ObjectList"].extend(OLextra)
            else:
                RESULT["ObjectList"] == OLextra

    if RESULT["ObjectList"] != None:
        
        # Initialise ProdStep vector:
        for x in RESULT["ObjectList"]:
            ProdStep.append({"Name": x["Name"], "Step": 0})

    # ===== LIAISON ===== #
    RESULT["Liaison"] = icYAML["Liaison"]

    if "LiExtra" in icYAML:

        LIextra = []

        for x in icYAML["LiExtra"]:

            if x["Child"] in li:
                LIextra.append(x)

        if len(LIextra) > 0:

            if RESULT["Liaison"] != None:
                RESULT["Liaison"].extend(LIextra)
            else:
                RESULT["Liaison"] == LIextra

    return(RESULT)

# ========================================================================================= #
# =================================== CLASSES/FUNCTIONS =================================== #
# ========================================================================================= #

# ========================================================================================= #
# Calculate DIFFERENCE -> Product POSITIONORIENTATION changed?
def CalculateDif_PROD(A,B):

    RES = False

    DIFx = B.x - A.x
    if (abs(DIFx) > 0.01):
        RES = True
    
    DIFy = B.y - A.y
    if (abs(DIFy) > 0.01):
        RES = True
    
    DIFz = B.z - A.z
    if (abs(DIFz) > 0.01):
        RES = True
    
    DIFqx = B.qx - A.qx
    if (abs(DIFqx) > 0.1):
        RES = True
    
    DIFqy = B.qy - A.qy
    if (abs(DIFqy) > 0.1):
        RES = True
    
    DIFqz = B.qz - A.qz
    if (abs(DIFqz) > 0.1):
        RES = True
    
    DIFqw = B.qw - A.qw
    if (abs(DIFqw) > 0.1):
        RES = True
    
    return(RES)

# ========================================================================================= #
# GetRecipe FUNCTION:
def GetRecipe(FOLDER, RECIPE_ID):
    
    RECIPE = {"Exists": True}
    
    PATH = os.path.join(get_package_share_directory('r3m_apg'), 'apg', 'recipes', FOLDER)
    RECIPE_PATH = PATH + "/" + str(RECIPE_ID) + ".yaml"
    
    if not os.path.exists(RECIPE_PATH):
        RECIPE["Exists"] = False
        return (RECIPE)

    # Get RECIPE VALUES:
    with open(RECIPE_PATH, 'r') as YAML:
        RecipeYAML = yaml.safe_load(YAML)
      
    RECIPE["usecase"] = RecipeYAML["Information"]["UseCase"]
    RECIPE["name"] = RecipeYAML["Information"]["Recipe"]
    
    RECIPE["id"] = RecipeYAML["id"] 
    RECIPE["type"] = RecipeYAML["type"]
    RECIPE["speed"] = RecipeYAML["speed"]

    RECIPE["pose"] = {}
      
    if (RECIPE["type"] == "PTP" or RECIPE["type"] == "LIN"):
        
        # GET -> POSITION:
        
        POSITION = {}
        POSITION["type"] = RecipeYAML["pose"]["position"]["type"]

        if POSITION["type"] == "DYNAMIC":
            
            POSITION["topic"] = RecipeYAML["pose"]["position"]["topic"]
            
            T = Pose()
            T.x = RecipeYAML["pose"]["position"]["transform"]["x"]
            T.y = RecipeYAML["pose"]["position"]["transform"]["y"]
            T.z = RecipeYAML["pose"]["position"]["transform"]["z"]
            POSITION["transform"] = T

        else:
            
            P = Pose()
            P.x = RecipeYAML["pose"]["position"]["pose"]["x"]
            P.y = RecipeYAML["pose"]["position"]["pose"]["y"]
            P.z = RecipeYAML["pose"]["position"]["pose"]["z"]
            POSITION["pose"] = P

        RECIPE["pose"]["position"] = POSITION

        # GET -> ORIENTATION:

        ORIENTATION = {}
        ORIENTATION["type"] = RecipeYAML["pose"]["orientation"]["type"]

        if ORIENTATION["type"] == "DYNAMIC":
            
            ORIENTATION["topic"] = RecipeYAML["pose"]["orientation"]["topic"]
            
            T = Pose()
            T.qx = RecipeYAML["pose"]["orientation"]["transform"]["qx"]
            T.qy = RecipeYAML["pose"]["orientation"]["transform"]["qy"]
            T.qz = RecipeYAML["pose"]["orientation"]["transform"]["qz"]
            T.qw = RecipeYAML["pose"]["orientation"]["transform"]["qw"]
            ORIENTATION["transform"] = T

        else:
            
            P = Pose()
            P.qx = RecipeYAML["pose"]["orientation"]["pose"]["qx"]
            P.qy = RecipeYAML["pose"]["orientation"]["pose"]["qy"]
            P.qz = RecipeYAML["pose"]["orientation"]["pose"]["qz"]
            P.qw = RecipeYAML["pose"]["orientation"]["pose"]["qw"]
            ORIENTATION["pose"] = P

        RECIPE["pose"]["orientation"] = ORIENTATION
    
    elif RECIPE["type"] == "GRIP":
        
        RECIPE["action"] = RecipeYAML["action"]
        RECIPE["value"] = RecipeYAML["value"]

    elif RECIPE["type"] == "VACUUM":
        
        RECIPE["action"] = RecipeYAML["action"]
        
    return(RECIPE)

# ========================================================================================= #
# ExecuteSkill_SERVER CLASS:
class ExecuteSkill_SERVER(Node):
    
    def __init__(self, INFO, ROB, OL, LI):
        
        # Robot -> {Model - Link - EEType - Package - InitialPose - HomePose}
        # ObjectList -> [{Name - Link - CADFile - Package - InitialPose - CurrentPose - PreviousPose}, ..]
        
        # CHECK if Object and Liaison arrays are not NULL:
        self.OLCheck = False
        if OL != None:
            self.OLCheck = True
        else:
            self.ObjectList = []
        self.LICheck = False
        if LI != None:
            self.LICheck = True

        # INITIALISE -> CLASSES needed for the Skill Execution:
        
        # PERCEPTION class:
        self.PERCEPTION = R3MPerceptionClient()
        
        # ===== OBJECTS (R3M_Perception) ===== #
        if self.OLCheck:
            self.OBJ = []
            for x in OL:
                self.OBJ.append(x["Name"])
        else:
            self.OBJ = None
        
        if self.OLCheck:
            self.OBJECTS = OBJECT(OL, R3MPerception=True)
            
        # ===== ROBOT CLASS ===== #
        self.ROBOT = RBT()
        self.ROBOTSTATE = ROB_STATE()
        
        # ===== END-EFFECTOR CLASS ===== #
        if ROB["EEType"] == "ParallelGripper":
            self.GRIPPER = parallelGR(self.OBJ, ROB["Model"], ROB["Link"])
        elif ROB["EEType"] == "VacuumGripper":
            self.GRIPPER = vacuumGR(self.OBJ, ROB["Model"], ROB["Link"])
        else:
            self.GRIPPER = None

        # INITIALISE -> GAZEBO SIMULATION ENVIRONMENT:
        self.ResetCond = {}
        self.ResetCond["Robot"] = ROB
        self.ResetCond["ObjectList"] = OL
        self.RESET = GzRESET(self.ResetCond, self.ROBOT, self.GRIPPER)
            
        # Launch -> R3M Perception OSD+M6D request:
        self.CAMERA = ROB["Camera"]["Gazebo"]
        
        if self.OLCheck:
            time.sleep(1.0)
            self.PERCEPTION.EXECUTE_PERCEPTION(self.OBJ, self.CAMERA)
            
        # Wait for -> R3M Perception M6D-RTI to start publishing Object Poses:
        self.OBJECTS.CheckObjectPose() # This is a blocking function that waits until M6D publishes to /ObjectPose/R3MPerception ROS 2 Topic.

        # Initialise VARIABLES using the information from the INPUT PARAMETERS:
        self.RecipeFolder = INFO["Name"]       # FOLDER to get the recipes from!
        
        # Initialise -> LIAISON CLASS:
        if self.LICheck:
            self.Liaison = LiaisonCheck(LI)

        # Initialise -> ObjectList class:
        if self.OLCheck:                
            self.ObjectList = self.OBJECTS.GetObjectPose() 

        # Initialise SERVICE SERVER:
        super().__init__('r3m_SkillExecution_ServiceServer')                                              
        self.srv = self.create_service(SkillExecution, "/r3m_SkillExecution", self.EXECUTE)
        
    def EXECUTE(self, request, response):
        
        global EEState, RobStep, ProdStep
        
        ID = request.id
        
        if (ID == 0):

            RES = self.RESET.RESET()
            response.result.id = 0
            
            if self.OLCheck:
                self.OBJECTS.ResetObjectList()
                
            # Reset -> R3M Perception (OSD + M6D-RTI nodes):
            self.R3MPerception_RESET()
                
            EEState = 1
            response.result.robstate.endeffector = EEState
            response.result.robstate.step = 0

            if self.OLCheck:
                ProdStep = []
                for x in self.ObjectList:
                    ProdStep.append({"Name": x["Name"], "Step": 0})

                self.ObjectList = self.OBJECTS.GetObjectPose()

            # RESET LIAISON:
            self.Liaison.RESET()
            liRES = self.Liaison.CHECK(self.ObjectList)
            response.result.liaison = liRES["LiaisonVector"]

            if RES == True:
                response.result.message = "ROS2 Environment RESET successful."
                response.result.success = True
                return(response)
            else:
                response.result.message = "ROS2 Environment RESET failed."
                response.result.success = False
                return(response)
            
        elif (ID == 100):

            # RESULT -> ID, exectime, error, message and success:
            response.result.id = 100
            response.result.success = True
            response.result.message = "R3M Perception ACTIVE SKILL executed. Liaison UPDATED."
            response.result.exectime = 0.0

            # RESULT -> Robot + EndEffector:
            response.result.robstate.robpose = self.ROBOTSTATE.GetRobotPose()
            response.result.robstate.step = RobStep
            response.result.robstate.endeffector = EEState
            
            # RE-START R3M Perception node:
            self.R3MPerception_RESET()

            # PRODUCT:
            if self.OLCheck:
                
                # GET ObjectList -> OBJECT POSES:
                OL = self.OBJECTS.GetObjectPose()
                self.ObjectList = OL
                PRODUCTS = []

                for x in OL:

                    P = Product()
                    P.name = x["Name"]

                    P.currentpose = Pose()
                    P.currentpose.x = x["CurrentPose"].x
                    P.currentpose.y = x["CurrentPose"].y
                    P.currentpose.z = x["CurrentPose"].z
                    P.currentpose.qx = x["CurrentPose"].qx
                    P.currentpose.qy = x["CurrentPose"].qy
                    P.currentpose.qz = x["CurrentPose"].qz
                    P.currentpose.qw = x["CurrentPose"].qw

                    P.previouspose = Pose()
                    P.previouspose.x = x["PreviousPose"].x
                    P.previouspose.y = x["PreviousPose"].y
                    P.previouspose.z = x["PreviousPose"].z
                    P.previouspose.qx = x["PreviousPose"].qx
                    P.previouspose.qy = x["PreviousPose"].qy
                    P.previouspose.qz = x["PreviousPose"].qz
                    P.previouspose.qw = x["PreviousPose"].qw

                    P.error = 0.0 # Error when retrieving from Gazebo is null.

                    DIF = CalculateDif_PROD(P.currentpose,P.previouspose)
                    if (DIF == True):

                        for y in ProdStep:
                            if P.name == y["Name"]:
                                y["Step"] = y["Step"] + 1
                                P.step = y["Step"]
                                break

                    else:
                        
                        for y in ProdStep:
                            if P.name == y["Name"]:
                                P.step = y["Step"]
                                break

                    PRODUCTS.append(P)

                response.result.product = PRODUCTS

            # LIAISON:
            if self.LICheck:
                    
                # GET LIAISON VECTOR:
                liRES = self.Liaison.CHECK(self.ObjectList)
                response.result.liaison = liRES["LiaisonVector"]

                # GET -> TASK FINISHED?
                if liRES["allMET"]:
                    response.result.finish = 1
                else:
                    None

            return(response)
        
        else:

            # Get RECIPE VALUES:
            RECIPE = GetRecipe(self.RecipeFolder, ID)

            if RECIPE["Exists"] == True:

                # Robot -> Check MOVEMENT TYPE and EXECUTE ACCORDINGLY:
                if (RECIPE["type"] == "PTP" or RECIPE["type"] == "LIN"):

                    RES = CALCULATE_RobPose(RECIPE["pose"], self.ObjectList)
                    if RES["Success"]:
                        RES = self.ROBOT.RobMove_EXECUTE(RECIPE["type"], RECIPE["speed"], RES["Pose"])

                    # If movement is successful:
                    if RES["Success"]:
                        RobStep = ID

                # ParallelGripper:
                elif (RECIPE["type"] == "GRIP"):

                    if RECIPE["action"] == "CLOSE":
                        RES = self.GRIPPER.CLOSE(RECIPE["value"])
                        
                        if RES["Success"]:
                            EEState = 0
                        
                    else:
                        RES = self.GRIPPER.OPEN()
                        
                        if RES["Success"]:
                            EEState = 1
                
                # VacuumGripper:
                elif (RECIPE["type"] == "VACUUM"):
                    
                    if RECIPE["action"] == "ACTIVATE":
                        RES = self.GRIPPER.ACTIVATE()
                        
                        if RES["Success"]:
                            EEState = 0
                        
                    elif RECIPE["action"] == "DEACTIVATE":
                        RES = self.GRIPPER.DEACTIVATE()
                        
                        if RES["Success"]:
                            EEState = 1

                # ============================================ #
                # ========== SKILL EXECUTION RESULT ========== #

                # RESULT -> ID, exectime, error, message and success:
                response.result.id = ID
                response.result.success = RES["Success"]
                response.result.message = RES["Message"]
                response.result.exectime = RES["ExecTime"]

                # RESULT -> Robot + EndEffector:
                response.result.robstate.robpose = self.ROBOTSTATE.GetRobotPose()
                response.result.robstate.step = RobStep
                response.result.robstate.endeffector = EEState

                if self.OLCheck:
                    # GET ObjectList -> OBJECT POSES:
                    OL = self.OBJECTS.GetObjectPose()
                    self.ObjectList = OL
                    PRODUCTS = []

                    for x in OL:

                        P = Product()
                        P.name = x["Name"]

                        P.currentpose = Pose()
                        P.currentpose.x = x["CurrentPose"].x
                        P.currentpose.y = x["CurrentPose"].y
                        P.currentpose.z = x["CurrentPose"].z
                        P.currentpose.qx = x["CurrentPose"].qx
                        P.currentpose.qy = x["CurrentPose"].qy
                        P.currentpose.qz = x["CurrentPose"].qz
                        P.currentpose.qw = x["CurrentPose"].qw

                        P.previouspose = Pose()
                        P.previouspose.x = x["PreviousPose"].x
                        P.previouspose.y = x["PreviousPose"].y
                        P.previouspose.z = x["PreviousPose"].z
                        P.previouspose.qx = x["PreviousPose"].qx
                        P.previouspose.qy = x["PreviousPose"].qy
                        P.previouspose.qz = x["PreviousPose"].qz
                        P.previouspose.qw = x["PreviousPose"].qw

                        P.error = 0.0 # Error when retrieving from Gazebo is null.

                        DIF = CalculateDif_PROD(P.currentpose,P.previouspose)
                        if (DIF == True):

                            for y in ProdStep:
                                if P.name == y["Name"]:
                                    y["Step"] = y["Step"] + 1
                                    P.step = y["Step"]
                                    break

                        else:
                            
                            for y in ProdStep:
                                if P.name == y["Name"]:
                                    P.step = y["Step"]
                                    break

                        PRODUCTS.append(P)

                    response.result.product = PRODUCTS

                if self.LICheck:
                    
                    # GET LIAISON VECTOR:
                    liRES = self.Liaison.RETURN()
                    response.result.liaison = liRES["LiaisonVector"]

                return(response)

            else:

                response.result.id = ID
                response.result.message = "ERROR. Recipe N -> " + str(ID) + " does not exist."
                response.result.success = False
                return(response)
            
    def R3MPerception_RESET(self):
        
        # Close and re-start M6D Node:
        os.system("pkill -f M6D_server.py") 
        time.sleep(2.0)
        
        CMD = "gnome-terminal -- ros2 run r3m_perception M6D_server.py"
        print("[R3M Perception -M6D- NODE RESTART]: Executing command -> " + CMD)
        PROCESS = subprocess.Popen(CMD, shell=True)
        
        # Re-start OSD+M6D-RTI:
        if self.OLCheck:
            self.PERCEPTION.EXECUTE_PERCEPTION(self.OBJ, self.CAMERA)
            self.OBJECTS.CheckObjectPose()

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
    
    # Multi-Threaded EXECUTOR:
    EXECUTOR = MultiThreadedExecutor()

    # === INITIAL CONDITIONS === #
    # Get ROS2 Parameter value:
    CONFIG = AssignArgument("config")
    if CONFIG != None:
        None
    else:
        print("")
        print("ERROR: config INPUT ARGUMENT has not been defined. Please try again.")
        print("Closing... BYE!")
        exit()

    # Get UseCase from yaml file:
    IC = GetIC_YAML(CONFIG)

    # Initialise NODE:
    if IC["Success"]:
        r3mNode = ExecuteSkill_SERVER(IC["UseCaseInfo"], IC["Robot"], IC["ObjectList"], IC["Liaison"])
        r3mNode.get_logger().info("[R3M Cell] - /ExecuteSkill ROS2 Service Server running, ROS2 node generated.")
        
        EXECUTOR.add_node(r3mNode)

        try:
            # Spin the executor to process callbacks
            EXECUTOR.spin()
        except KeyboardInterrupt:
            r3mNode.get_logger().info("[R3M Cell] - Shutting down due to keyboard interrupt.")
        finally:
            # Clean up when shutting down
            r3mNode.destroy_node()
            rclpy.shutdown()

    else:
        r3mNode = rclpy.create_node('R3M_RecipeExecution_Node')
        r3mNode.get_logger().info("[R3M Cell] - UseCase file not existing for the ROBOT CONFIGURATION selected. Closing r3m_RecipeExecution node.")
        
        # Clean up
        r3mNode.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()