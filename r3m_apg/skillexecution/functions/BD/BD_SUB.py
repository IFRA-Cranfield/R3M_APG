# Import libraries:
import rclpy
from rclpy.node import Node
from r3m_data.msg import Bd    

import time, threading, sys, os, yaml
from objectpose_msgs.msg import ObjectPose
from ament_index_python.packages import get_package_share_directory

# ===== EVALUATE INPUT ARGUMENTS ===== #         
def AssignArgument(ARGUMENT):
    ARGUMENTS = sys.argv
    for y in ARGUMENTS:
        if (ARGUMENT + ":=") in y:
            ARG = y.replace((ARGUMENT + ":="),"")
            return(ARG)

# Create NODE:
class SUBSCRIBER(Node):

    def __init__(self, CELL):

        self.CELL = CELL

        # Declare NODE:
        super().__init__("r3m_BD_SUBSCRIBER")      

        # Declare SUBSCRIBER:
        self.btSUB = self.create_subscription(Bd, "r3m_BD", self.CALLBACK_FN, 10)                                        
        
        # Declare PUBLISHER:
        self.PUBList = []
        for i in range(5):
            TopicName = "/Battery" + str(i+1) + "/ObjectPoseEstimation"
            self.SUBList.append(self.create_publisher(Bd, TopicName, 10))

        # Declare BATTERIES:
        self.BATTERIES = [0,0,0,0,0]
        self.DETECTED = None

    def CALLBACK_FN(self, detBT):
        self.DETECTED = detBT

    def updateBATTERIES(self):

        T = time.time() + 0.5
        while time.time() < T:
            rclpy.spin_once(self, timeout_sec=1.0)

        if self.DETECTED == None:
            self.DETECTED = [0,0,0,0,0]

        TH = threading.Thread(target=self.PUBLISH, daemon=True)
        TH.start()

        return()

    def PUBLISH(self):

        # === UPDATE === #

        T = time.time() + 5.0
        while time.time() < T:

            # Unassign if battery is gone:
            for i, BT_OLD in enumerate(self.BATTERIES):

                if BT_OLD not in self.DETECTED:
                    self.BATTERIES[i] = 0
            
            # Assign new batteries:
            for BT_NEW in self.DETECTED:

                # Check if it is already assigned:
                ASSIGNED = False
                for BT_OLD in self.BATTERIES:

                    if BT_NEW == BT_OLD:
                        ASSIGNED = True 

                # If not assigned -> ASSIGN:
                if not ASSIGNED:

                    for i, BT_OLD in enumerate(self.BATTERIES):

                        if BT_OLD == 0:
                            self.BATTERIES[i] = BT_NEW
                            break

            # === CONVERT === #
            self.BATTERIES_POSE = GetPose(self.BATTERIES, self.CELL)

            # === PUBLISH === #
            for i in range(5):
                self.PUBList[i].publish(self.BATTERIES_POSE[i])

        return()

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

    # Initialise NODE:
    rclpy.init(args=args)
    NODE = SUBSCRIBER(CELLname)
    print ("r3m_BD_SUBSCRIBER ROS2 node generated.")
    print ("")

    print("Detecting batteries and publishing the pose to ROS 2 Topics...")
    NODE.updateBATTERIES()

    # Close NODE:
    NODE.destroy_node
    rclpy.shutdown()

if __name__ == '__main__':
    main()

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
            YAML_PATH = PATH + "/r3mcell_cu_15.yaml"
        else:
            YAML_PATH = PATH + "/r3mcell_cu_24.yaml"

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