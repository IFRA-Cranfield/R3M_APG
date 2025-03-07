# R3M Research Project - R3M-APG (Automated Program Generation)

## Program Execution

This folder contains a series of programs (static sequences) that execute different use-case applications that have been used thoughout the R3M Research Project. Programs are executed using ROS 2-Python and the method is explained with more detail in [ros2_SimRealRobotControl - Program Execution](https://github.com/IFRA-Cranfield/ros2_SimRealRobotControl/blob/humble/instructions/ProgramExecution.md).

To execute a program, use the following command:

```sh
ros2 run ros2srrc_execution ExecuteProgram.py package:=r3m_apg program:="PROGRAM_NAME"
# PROGRAM_NAME: The name of the program you want to execute (without the .yaml extension).
```