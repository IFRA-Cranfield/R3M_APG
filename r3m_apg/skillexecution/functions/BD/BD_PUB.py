#!/usr/bin/python3

# Import libraries (PUBLISHER):

#  Import libraries:
import rclpy
from rclpy.node import Node
from r3m_data.msg import Bd    

from std_srvs.srv import Empty
from objectpose_msgs.msg import ObjectPose
from aux import GetPose   

# Import libraries (YOLO):
import os, sys, time
import cv2
from ultralytics import YOLO

from aux import GetSlot

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
    btFOUND = False

    # RUN -> YOLO PREDICTION:
    while True:

        ret, inputIMG = CAMERA.read()

        if inputIMG is not None:

            # PREDICT with YOLO and visualize:
            PREDICTION = YOLOmodel.predict(inputIMG, verbose=False)
            
            '''
            TITLE_0 = "R3M-APG - BD YOLO DETECTION"
            cv2.imshow(TITLE_0, PREDICTION[0].plot())

            key = cv2.waitKey(frame_delay)
            if key == ord('e'):
                cv2.destroyWindow(TITLE_0)
                break
            '''

            BATTERIES_DETECTED = []

            # PROCESS YOLO OUTPUT:
            for R in PREDICTION:

                boxes = R.boxes

                for box in boxes:

                    C = int(box.cls)
                    NAME = YOLOmodel.names[C]

                    if (NAME == "battery"):
                        btFOUND = True

                    # GET -> CASE COORDINATES:
                    if (NAME == "case") and (box.conf.item() > 0.75) and (caseFOUND == False) and (btFOUND == True):

                        Xleft_c, Ytop_c, Xright_c, Ybottom_c = box.xyxy[0]

                        if (270 > Xleft_c > 240) and (330 > Ytop_c > 300):

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

                        # VISUALIZE B.SLOT NUMBER IN RESULT:
                        B = box.xyxy[0] # Detected object's BOUNDING BOX.
                        cv2.rectangle(inputIMG, (int(B[0]), int(B[1])), (int(B[2]), int(B[3])), (0,0,0), 2)
                        LABEL = "BATTERY -> " + str(BATTERY_POS)
                        cv2.putText(inputIMG, LABEL, (int(B[0]), int(B[1]) - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,0), 2)

                        if BATTERY_POS not in BATTERIES_DETECTED:
                            BATTERIES_DETECTED.append(BATTERY_POS)

            print("Detected Batteries in this frame:")
            print(BATTERIES_DETECTED)
            
            # PUBLISH:
            MSG = Bd()
            MSG.batteries = BATTERIES_DETECTED
            NODE.PUB.publish(MSG)

            TITLE_1 = "R3M-APG - BD YOLO DETECTION and SLOT ESTIMATION"
            cv2.imshow(TITLE_1, inputIMG)

            key = cv2.waitKey(frame_delay)
            if key == ord('e'):
                cv2.destroyWindow(TITLE_1)
                break

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