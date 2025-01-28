# Import libraries (PUBLISHER):
import rclpy
from rclpy.node import Node
from r3m_data.msg import Bd       

# Import libraries (YOLO):
import os, sys
import cv2
from ultralytics import YOLO

# Create NODE:
class PUBLISHER(Node):

    def __init__(self):

        # Declare NODE:
        super().__init__("r3m_BD_PUBLISHER")                                              
        
        # Declare PUBLISHER:
        self.PUB = self.create_publisher(Bd, "r3m_BD", 10)

# ===== EVALUATE INPUT ARGUMENTS ===== #         
def AssignArgument(ARGUMENT):
    ARGUMENTS = sys.argv
    for y in ARGUMENTS:
        if (ARGUMENT + ":=") in y:
            ARG = y.replace((ARGUMENT + ":="),"")
            return(ARG)

# =================== MAIN =================== #
def main(args=None):

    print("")
    print(" --- Cranfield University --- ")
    print("        (c) IFRA Group        ")
    print("")

    print("R3M Automatic Program Generation/Execution.")
    print("Python script -> BD_PUB.py")
    print("")

    # Initialise NODE:
    rclpy.init(args=args)
    NODE = PUBLISHER()
    print ("r3m_BD_PUBLISHER ROS2 node generated.")
    print ("")

    # Get CELLname parameter value:
    CELLname = AssignArgument("cell")
    if CELLname != None:
        print("Cell model selected, for BD perception model execution -> "+ CELLname)
    else:
        print("")
        print("ERROR: cell INPUT ARGUMENT has not been defined. Please try again.")
        print("Closing... BYE!")
        exit()

    # (A) If using a VIDEO INPUT:
    '''
    pathVIDEO = os.path.join(os.path.expanduser('~'), 'Videos', 'OBS Studio') + "/BD_AMRC.mp4"
    CAMERA = cv2.VideoCapture(pathVIDEO)
    fps = CAMERA.get(cv2.CAP_PROP_FPS)
    frame_delay = int(1000 / fps)
    '''
    
    # (B) If using a CAMERA:
    CAMERA = cv2.VideoCapture(0)
    frame_delay = 1

    # Load custom YOLO MODEL:
    DIR = os.path.join(os.path.expanduser('~'), 'dev_ws', 'src', 'ros2_ObjectPoseEstimation', 'ros2_ope',  'yolo', 'models')
    if CELLname == "AMRC":
        modelPATH = DIR + "/BatteryDisassembly_AMRC.pt"
    else: 
        modelPATH = DIR + "/BatteryDisassembly_CU.pt"

    # YOLOmodel:
    YOLOmodel = YOLO(modelPATH)
    names = YOLOmodel.names
    print("The YOLO model will try to detect the following objects:")
    print(names)
    print("")

    caseFOUND = False

    # RUN -> YOLO PREDICTION:
    while True:

        ret, inputIMG = CAMERA.read()

        if inputIMG is not None:

            # PREDICT with YOLO and visualize:
            PREDICTION = YOLOmodel.predict(inputIMG, verbose=False)
            
            TITLE_0 = "R3M-APG - BD YOLO DETECTION"
            cv2.imshow(TITLE_0, PREDICTION[0].plot())

            key = cv2.waitKey(frame_delay)
            if key == ord('e'):
                cv2.destroyWindow(TITLE_0)
                break

            BATTERIES_DETECTED = []

            # PROCESS YOLO OUTPUT:
            for R in PREDICTION:

                boxes = R.boxes

                for box in boxes:

                    C = int(box.cls)
                    NAME = YOLOmodel.names[C]

                    # GET -> CASE COORDINATES:
                    if (NAME == "case") and (box.conf.item() > 0.75) and (caseFOUND == False):

                        Xleft_CASE, Ytop_CASE, Xright_CASE, Ybottom_CASE = box.xyxy[0] 
                        caseFOUND = True

                    # GET -> BATTERY COORDINATES:
                    if (NAME == "battery") and (box.conf.item() > 0.50) and (caseFOUND == True):
                        
                        Xleft, Ytop, Xright, Ybottom = box.xyxy[0]
                        
                        # GET -> RELATIVES, considering (0,0) is the case's TOP LEFT CORNER:
                        Xleft_CONV = int(Xleft) - int(Xleft_CASE)
                        Ytop_CONV = int(Ytop) - int(Ytop_CASE)
                        Xright_CONV = int(Xright) - int(Xright_CASE)
                        Ybottom_CONV = int(Ybottom) - int(Ybottom_CASE)

                        BATTERY_POS = GetSlot(Xleft_CONV,Ytop_CONV,CELLname)

                        print("BATTERY DETECTED:")
                        print(" - Xleft: " + str(Xleft_CONV) + " // Xright: " + str(Xright_CONV))
                        print(" - Ytop: " + str(Ytop_CONV) + " // Ybottom: " + str(Ybottom_CONV))
                        print(" - Battery is located in SLOT NUMBER -> " + str(BATTERY_POS))
                        print("")

                        if BATTERY_POS not in BATTERIES_DETECTED:
                            BATTERIES_DETECTED.append(BATTERY_POS)

            print("Detected Batteries in this frame:")
            print(BATTERIES_DETECTED)
            
            # PUBLISH:
            MSG = Bd()
            MSG.batteries = BATTERIES_DETECTED
            NODE.PUB.publish(MSG)

        else:
            print("Camera connection lost.")
            i = i + 1

            if i == 100:
                print("")
                print("Closing due to missing camera connectivity. BYE!")
                exit()

    print("")
    print("BD_PUB.py finalised.")
    print("Closing... BYE!")

    NODE.destroy_node
    rclpy.shutdown()

    exit()

if __name__ == '__main__':
    main()

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