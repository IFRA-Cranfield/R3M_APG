#!/usr/bin/python3
import sys
sys.dont_write_bytecode = True

# # # # # # # # # # # # # # # # # #                                  
#                                 #
#   ===== COPYRIGHT HERE =====    #
#                                 #
# # # # # # # # # # # # # # # # # #

# ========================================================================================= #
# ======================================== INCLUDE ======================================== #
# ========================================================================================= #

# System:
import os, sys, time

# ROS2:
import rclpy
from rclpy.node import Node
from ament_index_python.packages import get_package_share_directory

# Import -> OSD ROS 2 DATA:
from r3m_perception_data.srv import MegaPose
from r3m_perception_data.srv import OneShotDet
from objectpose_msgs.msg import ObjectPose

# R3M Perception PATH:
PATH_P = os.path.join(os.path.expanduser('~'), 'dev_ws', 'src', 'R3M_Perception', 'r3m_perception')

# Import FUNCTIONS:
PATH_F = PATH_P + "/python/functions"
sys.path.append(PATH_F)
# Import convertIMG:
from convertIMG import toROS2IMG_fromCV2
from convertIMG import toCV2_fromTOPIC
from convertIMG import toROS2IMG_fromTOPIC

# ========================================================================================= #
# ========================================================================================= #
# CLASSES -> OSD and M6D ROS 2 Service Clients:

# OSD NODE:
class OSDClient(Node):
    
    def __init__(self):
        
        super().__init__('r3m_OSDClient')
        self.cli = self.create_client(OneShotDet, "R3MPerception_OSD")
        
        while not self.cli.wait_for_service(timeout_sec=1.0):
            self.get_logger().info("[R3M Perception - OSDClient]: /R3MPerception_OSD ROS Service not available, waiting...")
        self.req = OneShotDet.Request()
        self.get_logger().info("[R3M Perception - OSDClient]: /R3MPerception_OSD ROS2.0 SERVICE detected!")

    def EXECUTE_OSD(self, IMG, CADList, CAM):
        
        self.get_logger().info("[R3M Perception - OSDClient]: Executing OSD Request...")

        self.req.cadlist = CADList
        self.req.camera = CAM
        self.req.img = IMG
        
        self.future = self.cli.call_async(self.req)    
         
# M6D NODE:
class M6DClient(Node):
    
    def __init__(self):
        
        super().__init__('r3m_M6DClient')
        self.cli = self.create_client(MegaPose, "R3MPerception_M6D")
        self.cli2 = self.create_client(MegaPose, "R3MPerception_M6DRTI")
        
        while not self.cli.wait_for_service(timeout_sec=1.0):
            self.get_logger().info("[R3M Perception - M6DClient]: /R3MPerception_M6D ROS Service not available, waiting...")
        self.get_logger().info("[R3M Perception - M6DClient]: /R3MPerception_M6D ROS2.0 SERVICE detected!")
        
        while not self.cli2.wait_for_service(timeout_sec=1.0):
            self.get_logger().info("[R3M Perception - M6DClient]: /R3MPerception_M6DRTI ROS Service not available, waiting...")
        self.get_logger().info("[R3M Perception - M6DClient]: /R3MPerception_M6DRTI ROS2.0 SERVICE detected!")
        
        self.req = MegaPose.Request()

    def EXECUTE_M6D(self, IMG, CAM, INPUT):
        
        self.get_logger().info("[R3M Perception - M6DClient]: Executing M6D Request...")
        
        self.req.input = INPUT
        self.req.camera = CAM
        self.req.img = IMG
        
        self.future = self.cli.call_async(self.req)
        
    def EXECUTE_RTI(self, IMG, CAM, INPUT):
        
        self.get_logger().info("[R3M Perception - M6DClient]: Executing M6D-RTI Request...")
        
        self.req.input = INPUT
        self.req.camera = CAM
        self.req.img = IMG
        
        self.future2 = self.cli2.call_async(self.req)

# CLASS -> R3MPerceptionClient:
class R3MPerceptionClient():
    
    def __init__(self):
        
        self.OSDNode = OSDClient()
        self.M6DNode = M6DClient()
        
        self.RTINode = None
        
    def EXECUTE_OSD(self, IMG, CAMERA, OBJECTS):
        
        self.OSDNode.EXECUTE_OSD(IMG, OBJECTS, CAMERA)

        while rclpy.ok():
            rclpy.spin_once(self.OSDNode)
            
            if self.OSDNode.future.done():
                try:
                    response = self.OSDNode.future.result()
                except Exception as exc:
                    self.OSDNode.get_logger().info("[R3M Perception - OSDClient]: Service call failed -> " + str(exc))
                else:
                    
                    self.OSDNode.get_logger().info("[R3M Perception - OSDClient]: ROS 2 Service Call executed. RESULTS:")
                    
                    # LOG RESULTS:
                    if response.success == False:
                        self.OSDNode.get_logger().info("[R3M Perception - OSDClient]: OSD Execution Failed.")
                    else:
                        for x in response.result:
                            self.OSDNode.get_logger().info("  - Object Name: "+ x.cadname)
                            self.OSDNode.get_logger().info("    Detection Successful? " + str(x.success))
                            self.OSDNode.get_logger().info("    Detection Score: " + str(x.score))
                            self.OSDNode.get_logger().info("    Bounding Box -> [tlx: "+str(x.tlx)+", tly: "+str(x.tly)+", brx: "+str(x.brx)+", bry: "+str(x.bry)+"]")
                    
                break
            
        return(response)
    
    def EXECUTE_M6D(self, IMG, CAMERA, INPUT_M6D):
        
        self.M6DNode.EXECUTE_M6D(IMG, CAMERA, INPUT_M6D)

        while rclpy.ok():
            rclpy.spin_once(self.M6DNode)
            
            if self.M6DNode.future.done():
                try:
                    response = self.M6DNode.future.result()
                except Exception as exc:
                    self.M6DNode.get_logger().info("[R3M Perception - M6DClient]: Service call failed -> " + str(exc))
                else:
                    
                    self.M6DNode.get_logger().info("[R3M Perception - M6DClient]: ROS 2 Service Call executed. RESULTS:")
                
                    for x in response.result:
                        self.M6DNode.get_logger().info("  - Object Name: "+ x.objectname)
                        self.M6DNode.get_logger().info("    x -> " + str(x.x))
                        self.M6DNode.get_logger().info("    y -> " + str(x.y))
                        self.M6DNode.get_logger().info("    z -> " + str(x.z))
                        self.M6DNode.get_logger().info("    qx -> " + str(x.qx))
                        self.M6DNode.get_logger().info("    qy -> " + str(x.qy))
                        self.M6DNode.get_logger().info("    qz -> " + str(x.qz))
                        self.M6DNode.get_logger().info("    qw -> " + str(x.qw))
                break
            
        return(response)
    
    def EXECUTE_RTI(self, IMG, CAMERA, INPUT_M6D):
        
        self.M6DNode.EXECUTE_RTI(IMG, CAMERA, INPUT_M6D)
        rclpy.spin_once(self.M6DNode, timeout_sec=1.0)
        return()
    
    def EXECUTE_PERCEPTION(self, OBJECTS, CAMERA):
        
        # Initialise -> RTINode + RESULT variables:
        
        RESULT = {}
        RESULT["Success"] = False
        
        if self.RTINode is not None:
            self.RTINode.destroy_node()
            self.RTINode = None
            
        # GET -> FRAME:
        CAMERATopic = CAMERA + "/image_raw"
        IMG_ROS2 = toROS2IMG_fromTOPIC(CAMERATopic)
            
        # Execute -> OSD:
        print("[R3M Perception] - One-Shot Detection: Execution in progress...")
        OSD_RES = self.EXECUTE_OSD(IMG_ROS2, CAMERA, OBJECTS)
        
        if OSD_RES.success == False:
            print("[R3M Perception] - OSD Execution failed.")
            return(RESULT)
        else:
            print("[R3M Perception] - OSD Execution successful.")
            for x in OSD_RES.result:
                print("  - Object Name: "+ x.cadname)
                print("    Detection Successful? " + str(x.success))
                print("    Detection Score: " + str(x.score))
                print("    Bounding Box -> [tlx: "+str(x.tlx)+", tly: "+str(x.tly)+", brx: "+str(x.brx)+", bry: "+str(x.bry)+"]")
                print("")
        
        # Execute -> M6D:
        print("[R3M Perception] - Megapose6D: Execution in progress...")
        self.EXECUTE_RTI(IMG_ROS2, CAMERA, OSD_RES.result)
        print("[R3M Perception] - Megapose6D: Execution request sent!")
        
        return()
    
# For testing purposes:
# ========================================================================================= #
# ========================================= MAIN ========================================== #
# ========================================================================================= #
def main(args=None):
    
    rclpy.init(args=args)
    
    Perception = R3MPerceptionClient()
    print("")
    
    ObjectList = ["adapter_plate_triangular", "adapter_plate_square"]
    Camera = "lenovoFHD_gazebo"
    
    Perception.EXECUTE_PERCEPTION(ObjectList, Camera)
    
if __name__ == '__main__':
    main()