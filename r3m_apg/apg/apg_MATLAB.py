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
import os
import time

# ROS2:
import rclpy
from rclpy.node import Node
from ament_index_python.packages import get_package_share_directory

# CUSTOM ROS2 MSG/SRV/ACTION:
from ros2srrc_data.msg import Robpose
from r3m_data.srv import SkillExecution

# Required for MATLAB AGENT EXECUTION:
import numpy as np
import matlab.engine

# ========================================================================================= #
# Execute Skill -> ROS 2 Service Client:
class R3MSkillClient(Node):

    def __init__(self):

        # Initialise ROS2 Node:
        super().__init__('r3m_APGMatlab_SkillClient')

        # Create ROS2 Service Client:
        self.cli_SKILL = self.create_client(SkillExecution, "/r3m_SkillExecution")  

        # Declare REQUEST variable (of CUSTOM DATA type):
        self.req_SKILL = SkillExecution.Request()  

    def SKILL_REQUEST(self, ID):
        
        self.req_SKILL.id = ID
        self.future_SKILL = self.cli_SKILL.call_async(self.req_SKILL)

# FUNCTION -> EXECUTE SKILL:
def ExecuteSkill(CLIENT, ID):

    CLIENT.SKILL_REQUEST(ID)
    while rclpy.ok():
        rclpy.spin_once(CLIENT)
        if CLIENT.future_SKILL.done():
            try:
                skillRES = CLIENT.future_SKILL.result().result
            except Exception as exc:
                print("[R3M Cell] - /ExecuteSkill ROS2 Service call failed. ERROR: " + str(exc))
                return(False)
            else:
                print("[R3M Cell] - /ExecuteSkill RESULT:")
                print(skillRES)
                print("")
            break

    return(skillRES)
        
# ========================================================================================= #
# MatlabAgent:
class MatlabAgent():
    
    def __init__(self, UseCase):

        super().__init__()
        self.MATLAB = matlab.engine.start_matlab()
        
        self.PATH = os.path.join(get_package_share_directory('r3m_apg'), 'apg', 'agents')
        self.AGENT = UseCase + ".mat"
        
    def Execute(self, ID, RobState, EEState, ObjState, ObjectNO):
        
        # ASSIGN -> Input values to AGENT:

        if ObjectNO == 1:
            observation = [ID, RobState, EEState, ObjState[0]]
        elif ObjectNO == 2:
            observation = [ID, RobState, EEState, ObjState[0], ObjState[1]]
        
        observation = np.array(observation)
        
        self.MATLAB.addpath(self.PATH)
        var = self.MATLAB.evaluatePolicy(observation, self.AGENT)
        
        return(var)
        
# ========================================================================================= #
# ========================================= MAIN ========================================== #
# ========================================================================================= #

def main(args=None):
    
    rclpy.init(args=args)
    
    # PRINT:
    print("==========================================================")
    print("R3M - AUTOMATIC PROGRAM GENERATION: Execution of APG Agent")
    print("")

    # INPUT PARAMETERS:
    ObjectNO = 2
    UseCase = "CubeStacking"

    # INITIALISE ROS 2 Classes:
    Node_SkillExecution = R3MSkillClient()
    APG_Agent = MatlabAgent(UseCase)
    
    # INITIAL STATE -> Recipe N1 will be executed as a initial step, to get the state of the system:
    print("Initialising RLA: Executing Recipe N1...")
    skillRESULT = ExecuteSkill(Node_SkillExecution, 1)
    
    ID = 0
    
    RobState = skillRESULT.robstate.step
    EEState = skillRESULT.robstate.endeffector
    
    ObjState = []
    for i in range(ObjectNO):
        ObjState.append(skillRESULT.product[i].step)
    
    CONTINUE = True
    while CONTINUE:
        
        print("RECIPE EXECUTION: Getting Recipe ID from RLA...")
        
        print("Robot State: " + str(RobState))
        print("End Effector State: " + str(EEState))

        print("Object State:")
        for i in range(ObjectNO):
            print("- Object N" + str(i+1) + ", " + skillRESULT.product[i].name + " -> " + str(ObjState[i]))

        print("")
        
        # GET -> RECIPE ID from AGENT:
        RECIPE = APG_Agent.Execute(ID, RobState, EEState, ObjState, ObjectNO)
        RECIPE_ID = int(RECIPE)
        
        print("RECIPE ID obtained! ")
        print("ID: " + str(RECIPE_ID))
        print("")
        
        print("Executing Recipe N" + str(RECIPE_ID) + "...")
        
        # EXECUTE -> RECIPE:
        skillRESULT = ExecuteSkill(Node_SkillExecution, RECIPE_ID)
            
        ID = float(skillRESULT.id)

        RobState = skillRESULT.robstate.step
        EEState = skillRESULT.robstate.endeffector
        
        ObjState = []
        for i in range(ObjectNO):
            ObjState.append(skillRESULT.product[i].step)

        # Check if -> LIAISON MET + ID=1, then FINISH!
        LI_MET = True
        for x in skillRESULT.liaison:

            if x.liaison_met:
                print("LIAISON MET! -> " + x.name)
            else:
                LI_MET = False

        print("")

        if ID == 1 and LI_MET == True:
            print("SUCCESS! All liaisons have been met and the Robot has returned to Home Position.")
            print("PROGRAM EXECUTION SUCCESSFULLY FINISHED!")
            print("")
            print("Closing program... BYE!")
            CONTINUE = False

    # FINISH:
    rclpy.shutdown()

if __name__ == '__main__':
    main()
