#!/usr/bin/python3

# Import libraries (PUBLISHER):

#  Import libraries:
import sys, time
import rclpy
from rclpy.node import Node
from r3m_data.msg import Bd    

from std_msgs.msg import String
from objectpose_msgs.msg import ObjectPose
from aux import GetPose   

from rclpy.executors import MultiThreadedExecutor

UPDATE = False

# ===== EVALUATE INPUT ARGUMENTS ===== #         
def AssignArgument(ARGUMENT):
    ARGUMENTS = sys.argv
    for y in ARGUMENTS:
        if (ARGUMENT + ":=") in y:
            ARG = y.replace((ARGUMENT + ":="),"")
            return(ARG)
        
# Create NODE_SUB:
class SUB_UPDATE(Node):

    def __init__(self):

        # Declare NODE:
        super().__init__("r3m_BD_SUBSCRIBER")  

        # Declare SUBSCRIBER:
        self.btSUB = self.create_subscription(String, "r3m_UPDATE", self.CALLBACK_FN, 1)     
        
    def CALLBACK_FN(self, MSG):

        if MSG.data == "UPDATE":

            global UPDATE
            UPDATE = True

# Create NODE_SUB:
class SUBSCRIBER(Node):

    def __init__(self, CELL, BATTERIES=[0,0,0,0,0]):

        # Declare NODE:
        super().__init__("r3m_BD_SUBSCRIBER")      

        # Declare SUBSCRIBER:
        self.btSUB = self.create_subscription(Bd, "r3m_BD", self.CALLBACK_FN, 1)      

         # Declare PUBLISHER:
        self.PUBList = []
        for i in range(5):
            TopicName = "/Battery" + str(i+1) + "/ObjectPoseEstimation"
            self.PUBList.append(self.create_publisher(ObjectPose, TopicName, 1))

        # Declare CELL+BATTERIES:
        self.CELL = CELL
        self.BATTERIES = BATTERIES                                  
        
    def CALLBACK_FN(self, detBT):

        global UPDATE

        DETECTED = detBT.batteries

        if UPDATE == True:

            BATTERIES = self.BATTERIES
            BATTERIES_OLD = self.BATTERIES

            if DETECTED == None:
                DETECTED = [0,0,0,0,0]

            # Unassign if battery is gone:
            for i, BT_OLD in enumerate(BATTERIES):

                if BT_OLD not in DETECTED:
                    BATTERIES[i] = 0
            
            # Assign new batteries:
            for BT_NEW in DETECTED:

                # Check if it is already assigned:
                ASSIGNED = False
                for BT_OLD in BATTERIES:

                    if BT_NEW == BT_OLD:
                        ASSIGNED = True 

                # If not assigned -> ASSIGN:
                if ASSIGNED == False:

                    for i, BT_OLD in enumerate(BATTERIES):

                        if BT_OLD == 0:
                            BATTERIES[i] = BT_NEW
                            break

                print("RESULT:")
                print("Detected:")
                print(DETECTED)
                print("Previous:")
                print(BATTERIES_OLD)
                print("Updated: ")
                print(BATTERIES)

                self.BATTERIES = BATTERIES
                UPDATE = False

        # === PUBLISH === #
        for i in range(5):
            
            BATTERIES_POSE = GetPose(self.BATTERIES, self.CELL)
            self.PUBList[i].publish(BATTERIES_POSE[i])
            
            print("Published ObjectPose: " )
            print(BATTERIES_POSE[i])
            print("")

# =================== MAIN =================== #
def main(args=None):

    print("")
    print(" --- Cranfield University --- ")
    print("        (c) IFRA Group        ")
    print("")

    print("R3M Automatic Program Generation/Execution.")
    print("Python script -> BD_SUB.py")
    print("")

    # Get CELLname parameter value:
    CELLname = AssignArgument("cell")
    if CELLname != None:
        print("Cell model selected, for BD perception model execution -> "+ CELLname)
    else:
        print("")
        print("ERROR: cell INPUT ARGUMENT has not been defined. Please try again.")
        print("Closing... BYE!")
        exit()

    rclpy.init(args=args)

    EXECUTOR = MultiThreadedExecutor()

    A = SUBSCRIBER(CELLname)
    EXECUTOR.add_node(A)
    B = SUB_UPDATE()
    EXECUTOR.add_node(B)
    
    EXECUTOR.spin()                                                                       

if __name__ == '__main__':
    main()