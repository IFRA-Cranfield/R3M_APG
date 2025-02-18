# R3M Research Project - R3M-APG Repository

## Installation Steps

The steps below must be followed in order to properly set-up a ROS 2 Humble machine which is needed for the usage of the ROS 2 Packages in the _R3M-APG_ repository. It is recommended to install Ubuntu 22.04 Desktop on your PC for an optimal performance, but a VM could be used for simple simulations and executions.

__REQUIRED: Install the ros2_SimRealRobotControl GitHub Repository__

The ROS 2 packages developed in R3M-APG are based on IFRA-Cranfield's [ros2_SimRealRobotControl](https://github.com/IFRA-Cranfield/ros2_SimRealRobotControl) GitHub Repository. Therefore, ros2_SimRealRobotControl must be installed in order to set-up R3M-APG in any Ubuntu 22.04 + ROS 2 Humble machine.

Installation steps can be found at: https://github.com/IFRA-Cranfield/ros2_SimRealRobotControl/blob/humble/instructions/Installation.md

__REQUIRED: Download and install the R3M_Cell Repository__

R3M-APG has been developed, implemented and tested for the R3M-Cell ROS 2 Environment. Therefore, the R3M-UK/R3M-Cell GitHub repository must be downloaded and installed for R3M-APG to work:

```sh
cd ~/dev_ws/src
git clone https://github.com/R3M-UK/R3M_Cell
cd ~/dev_ws
colcon build
```   

__Download and install the R3M_Perception Repository__

TBD.

__Download and install the R3M_OPE Repository__

TBD.

__Download and install R3M_APG__

```sh
cd ~/dev_ws/src
git clone https://github.com/R3M-UK/R3M_APG
cd ~/dev_ws
colcon build
```   