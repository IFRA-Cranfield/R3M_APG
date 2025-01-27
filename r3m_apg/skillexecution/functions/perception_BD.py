#!/usr/bin/python3

# # # # # # # # # # # # # # # # # #                                  
#                                 #
#   ===== COPYRIGHT HERE =====    #
#                                 #
# # # # # # # # # # # # # # # # # #

# ========================================================================================= #
# ======================================== INCLUDE ======================================== #
# ========================================================================================= #

# ===== IMPORT REQUIRED COMPONENTS ===== #
import os, sys

# Required to include ROS2 and its components:
import rclpy
from rclpy.node import Node

# ROS 2 data:
from objectpose_msgs.msg import ObjectPose
from sensor_msgs.msg import Image

# OpenCV:
import cv2
# ROS2 to OpenCV -> cv_bridge:
from cv_bridge import CvBridge, CvBridgeError

# YOLO:
from ultralytics import YOLO

# ===== EVALUATE INPUT ARGUMENTS ===== #         
def AssignArgument(ARGUMENT):
    ARGUMENTS = sys.argv
    for y in ARGUMENTS:
        if (ARGUMENT + ":=") in y:
            ARG = y.replace((ARGUMENT + ":="),"")
            return(ARG)

# ===== TRAIN MODEL ===== #
def main(args=None):

    print("")
    print(" --- Cranfield University --- ")
    print("        (c) IFRA Group        ")
    print("")

    print("R3M Automatic Program Generation/Execution.")
    print("Python script -> Pperception_BD.py")
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

    # Initialise -> ROS 2:
    rclpy.init()

    # If using a video input:
    pathVIDEO = os.path.join(os.path.expanduser('~'), 'Videos', 'OBS Studio') + "/BD_AMRC_bis.mp4"
    CAMERA = cv2.VideoCapture(pathVIDEO)
    fps = CAMERA.get(cv2.CAP_PROP_FPS)
    frame_delay = int(1000 / fps)
    
    # Initialise -> CAMERA:
    #CAMERA = cv2.VideoCapture(0)
    #frame_delay = 1

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

                        print("BATTERY DETECTED:")
                        print(" - Xleft: " + str(Xleft_CONV) + " // Xright: " + str(Xright_CONV))
                        print(" - Ytop: " + str(Ytop_CONV) + " // Ybottom: " + str(Ybottom_CONV))
                        print("")

        else:
            print("Camera connection lost.")

    print("")
    print("Object POSITION ESTIMATION finalised.")
    print("Closing... BYE!")

if __name__ == '__main__':
    main()