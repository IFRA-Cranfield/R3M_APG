# R3M Research Project - R3M-APG (Automated Program Generation)

## Automated Program Generation (APG) - Skill Execution

The /SkillExecution folder in the R3M-APG repository contains the scripts required to launch and manage the Automated Program Generation (APG) environment, which is responsible for executing robot tasks within the R3M-Cell. This environment enables the robot to perform various tasks by following predefined use-cases, each composed of a sequence of recipes. A recipe represents a structured set of robot skills, which are individual actions or movements required to complete a task. These robot skills are defined in the ros2_SimRealRobotControl package and are executed sequentially to achieve the desired process.

The execution of recipes is managed through a ROS 2 service called /r3m_SkillExecution, which acts as the interface between the APG environment and the robot. When a recipe is triggered, the corresponding robot skills are executed based on predefined parameters, ensuring that each step is carried out correctly within the robotic cell. This structured execution allows for flexibility in handling different use-cases while maintaining a standardized method for skill execution.

To accommodate different execution setups, the /SkillExecution/wrappers folder includes various Python scripts that initialize the APG environment according to the selected mode. These modes include simulation in Gazebo with internal perception, simulation with external perception systems, and execution on a real robot. The appropriate wrapper script ensures that the system initializes correctly, waiting for user input via a ROS 2 service call to begin executing robot skills.

Additionally, key scripts such as r3m_ROBOT.py, R3M_SIMULATION.py, and R3M_TRAIN.py are used to launch the full R3M ROS 2-based environment. These scripts handle the initialization of the ROS 2 Robot Simulation/Control environment, MoveIt!2 motion planning tool, and the perception system where applicable. Depending on the scenario, they ensure that the robot operates within a properly configured environment, whether in simulation or on a physical system, and avoid having to launch all the components one after the other in the terminal.

## R3M APG Environment: LAUNCH INSTRUCTIONS

### APG environment launch

This command launches the R3M Skill Execution ROS 2 node for Gazebo Simulation:

```sh
ros2 run r3m_apg r3m_SkillExecution_Gazebo.py train:="" perception:="" config:=""

# train:=True for when the APG Training pipeline is required, and train:=False for when the APG Execution is required.

# perception:=True for when an external perception system is being used (/ObjectPoseEstimation), and perception:=False for when the IFRA-Cranfield/ObjectPose GzPlugin is being used (/ObjectPose).

# config refers to the R3M Use-Case (e.g., "r3mcell_cu_13").
```

This command launches the R3M Skill Execution ROS 2 node for Gazebo Simulation, when R3M Perception (One-Shot Detection + Megapose6D) is being used:

```sh
ros2 run r3m_apg r3m_SkillExecution_Gz_Perception.py config:=""

# config refers to the R3M Use-Case (e.g., "r3mcell_cu_13").
```

This command launches the R3M Skill Execution ROS 2 node for the Real Robot:

```sh
ros2 run r3m_apg r3m_SkillExecution_RealRobot.py perception:="" config:=""

# perception:=True for when R3M Perception (One-Shot Detection + Megapose6D) is being used, and perception:=False for when any other perception system is being used (or for those cases where perception is not required at all).

# config refers to the R3M Use-Case (e.g., "r3mcell_cu_13").
```

This command launches the R3M Skill Execution ROS 2 node for the Real Robot (Battery Disassembly use-case):

```sh
ros2 run r3m_apg r3m_SkillExecution_RealRobot_BD.py config:="" cell:=""

# config refers to the R3M Use-Case (BD use-cases: r3mcell_cu_15 or r3mcell_amrc_24).

# cell is either "CRANFIELD" or "AMRC", depending on the cell used.
```

### APG + R3M-Cell environment launch

r3m_TRAIN, _SIMULATION and _ROBOT scrips have been developed to enable a simpler management of the R3M Environment. The commands below execute all the required components (Robot Control, MoveIt!2, APG, Perception...) by only running 1 command in 1 terminal window. In addition, a simple CTRL+C in the same running window terminates all the processes simultaneously.

This command launches the whole R3M Environment (CELL + APG) for the APG-RL agent training process in Gazebo Simulation:
```sh
ros2 run r3m_apg r3m_TRAIN.py package:="" config:=""

# package is either "r3mcell_cu" (CRANFIELD) or "r3mcell_amrc" (AMRC).

# config refers to the R3M Use-Case (e.g., "r3mcell_cu_13").
```

This command launches the whole R3M Environment (CELL + APG) in Gazebo Simulation:
```sh
ros2 run r3m_apg r3m_SIMULATION.py package:="" config:="" perception:=""

# package is either "r3mcell_cu" (CRANFIELD) or "r3mcell_amrc" (AMRC).

# config refers to the R3M Use-Case (e.g., "r3mcell_cu_13").

# perception:=r3m to launch the R3M Perception node (One-Shot Detection + Megapose6D) or perception:=MarkerGrid to launch the IFRA-Cranfield/ObjectPoseEstimation ROS 2 node.
```

This command launches the whole R3M Environment (CELL + APG) for the Real Robot:
```sh
ros2 run r3m_apg r3m_ROBOT.py package:="" config:="" perception:="" robot_ip:=0.0.0.0

# package is either "r3mcell_cu" (CRANFIELD) or "r3mcell_amrc" (AMRC).

# config refers to the R3M Use-Case (e.g., "r3mcell_cu_13").

# perception:=r3m to launch the R3M Perception node (One-Shot Detection + Megapose6D), perception:=MarkerGrid to launch the IFRA-Cranfield/ObjectPoseEstimation ROS 2 node or perception:=BD for the Battery Disassembly use-case.
```

## R3M Skill (Recipe) Execution

Once the R3M APG environment is up and running, any robot skill can be manually executed by calling the /r3m_SkillExecution ROS 2 Service in the terminal:
```sh
ros2 service call /r3m_SkillExecution r3m_data/srv/SkillExecution "{id: -}"

# You can check all the recipes for each R3M Use-Case in the R3M_APG/r3m_apg/recipes folder.
```