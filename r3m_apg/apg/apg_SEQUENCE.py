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
import sys

# ROS2:
import rclpy
from rclpy.node import Node

# CUSTOM ROS2 MSG/SRV/ACTION:
from r3m_data.srv import SkillExecution

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
                #print("[R3M Cell] - /ExecuteSkill ROS2 Service call failed. ERROR: " + str(exc))
                return(False)
            else:
                #print("[R3M Cell] - /ExecuteSkill RESULT:")
                #print(skillRES)
                #print("")
                None
            break

    return(skillRES)

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

    # Get SEQUENCE:
    SQ = AssignArgument("sequence")
    if SQ != None:
        SEQUENCE = SQ.split("-")
    else:
        print("")
        print("ERROR: sequence INPUT ARGUMENT has not been defined. Please try again.")
        print("Closing... BYE!")
        exit()
    
    rclpy.init(args=args)
    
    # PRINT:
    print("=============================================================")
    print("R3M - AUTOMATIC PROGRAM GENERATION: Execution of APG Sequence")
    print("")

    # INITIALISE ROS 2 Classes:
    Node_SkillExecution = R3MSkillClient()
    
    # INITIAL STATE -> Recipe N1 will be executed as a initial step, to get the state of the system:
    print("Initialising APG-Sequence execution: Executing Recipe N1...")
    print("")
    
    skillRESULT = ExecuteSkill(Node_SkillExecution, 1)

    print("Initial RobPose -> " + str(skillRESULT.robstate.robpose))
    print("Initial EEState -> " + str(skillRESULT.robstate.endeffector))
    print("Initial ObjectState: ")
    for i in skillRESULT.product:
        print("   - " + i.name + ": " + str(i.currentpose))

    print("")
    print("")
    
    ID = 0

    print("===== SEQUENCE EXECUTION =====")
    print("")

    k = 0
    for x in SEQUENCE:
        
        k=k+1

        print("STEP N" + str(k) + ": RECIPE N->" + str(x))
        print("Executing APG recipe... ")
        print("")

        skillRESULT = ExecuteSkill(Node_SkillExecution, int(x))

        print("Recipe execution complete! Results: ")
        print("Execution successful? -> " + str(skillRESULT.success))
        print("Feedback message: " + skillRESULT.message)
        print("RobPose -> " + str(skillRESULT.robstate.robpose))
        print("EEState -> " + str(skillRESULT.robstate.endeffector))
        print("ObjectState: ")
        for i in skillRESULT.product:
            print("   - " + i.name + ": " + str(i.currentpose))
        
        if skillRESULT.id == 100:
            print("LiaisonCheck: ")
            for i in skillRESULT.liaison:
                print("   - " + i.name + " -> DIFF("+ str(round(i.diff, 4)) +"), DIFFmax("+ str(round(i.diff_max,4)) +"), COMPLETE? -> " + str(i.liaison_met))

        print("")
        print("")

        if not skillRESULT.success:

            print("ERROR: Sequence execution failed in step number -> " + str(k) + ", recipe number -> " + str(x) + ". Closing program... BYE!")
            exit()

    print("SEQUENCE EXECUTION SUCCESSFULLY FINISHED. BYE!")

    # FINISH:
    rclpy.shutdown()

if __name__ == '__main__':
    main()
