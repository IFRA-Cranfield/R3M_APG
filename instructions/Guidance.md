# R3M Research Project - R3M-APG Practical Example

The following example demonstrates the practical use of the R3M-APG module within the R3M Research Project, focusing on the Cube Kitting use-case executed in the Cranfield University UR3 robot cell through Gazebo simulation. 

This workflow illustrates how the APG system integrates with the R3M architecture to autonomously generate, manage, and execute robotic programs. The example covers the complete process — from launching the ROS 2-based APG environment and executing predefined skills, to running a full use-case program and deploying a reinforcement learning (RL)-trained agent. An additional step showcases the integration of perception capabilities for object pose estimation, enabling adaptive and data-driven task execution within the simulated manufacturing environment.

## STEP 1: Launch R3M APG-ROS 2 Environment

The Cube Kitting use-case for the Cranfield University's UR3 Robot Cell is identified as: "r3mcell_cu_22"

Option 1 -> Launch R3M-Cell first, R3M-APG orchestrator later on another terminal shell:
```sh
# Launch the R3M Cell Environment:
ros2 launch ros2srrc_launch moveit2.launch.py package:=r3mcell_cu config:=r3mcell_cu_22

# Launch the R3M-APG Orchestrator:
ros2 run r3m_apg r3m_SkillExecution_Gazebo.py train:=False perception:=False config:=r3mcell_cu_22

# train:=False -> We are going to execute the use-case, not train the RL model.
# perception:=False -> We are going to get the exact object poses from Gazebo directly, using IFRA-Cranfield/ObjectPose plugin.
```

Option 2 -> Launch both components together using the r3m_SIMULATION.py script:
```sh
# Launch the R3M Cell + R3M APG environment:
ros2 run r3m_apg r3m_SIMULATION.py package:=r3mcell_cu config:=r3mcell_cu_22
```

After this step, you should have:
- Gazebo Simulation Environment open, with the UR3 Robot Cell.
- MoveIt!2 Framework w/ UR3 (+ Robotiq HandE gripper).
- 4 Coloured Cubes spawned, on top of the UR3 stand.
- The R3M-APG Orchestrator ready to receive commands.

### Explanation: Cube Kitting Use-Case

Before moving into the Skill and Program Execution sections, it is important to introduce the Cube Kitting use-case and explain the associated skill recipes and requirements (liaisons) necessary to complete it within the Cranfield University UR3 robot cell (Gazebo simulation).

The Cube Kitting use-case consists of a pick-and-place task where the robot must correctly position four coloured cubes — red, blue, green, and white — on top of their designated slots in a tray. This process is designed to demonstrate the full integration of motion, perception, and control within the R3M-APG framework. The task is considered successful once all four cubes are accurately placed, fulfilling the four liaisons (one per cube) that confirm correct spatial placement through perception feedback.

Each cube follows a structured skill recipe, composed of a sequence of motion and gripper operations defined in the r3mcell_cu_22 skill set. The general pick-and-place pattern is identical for all cubes and is defined as follows:

- Move to home pose (1.yaml)
- Move to pick approach
- Move to pick position
- Close gripper (6.yaml)
- Move back to pick approach
- Move to place approach
- Move to place position
- Open gripper (7.yaml)
- Move back to place approach
- Return to home pose (1.yaml)
- Execute perception check (100.yaml) to validate liaison completion

The specific skill files used for each cube are as follows:

- Red Cube: 12.yaml (move to pick-approach pose), 13.yaml (move to pick pose), 14.yaml (move to place-approach pose), 15.yaml (move to place pose)
- Blue Cube: 22.yaml, 23.yaml, 24.yaml, 25.yaml
- Green Cube: 32.yaml, 33.yaml, 34.yaml, 35.yaml
- White Cube: 42.yaml, 43.yaml, 44.yaml, 45.yaml

In each recipe, the approach and position pairs define the robot’s motion for both picking and placing actions. For instance, the red cube’s routine executes:
1 → 12 → 13 → 6 → 12 → 14 → 15 → 7 → 14 → 1 → 100, and this same logic applies to the blue (2X), green (3X), and white (4X) cubes.

By combining these individual skill sequences with the perception validation step, the Cube Kitting use-case demonstrates the ability of the R3M-APG framework to autonomously execute multi-step, sensor-informed tasks that replicate real manufacturing operations in a simulated environment.

## STEP 2: R3M Skill Execution

You can execute individual skills by making a ROS 2 service call to:
```sh
ros2 service call /r3m_SkillExecution r3m_data/srv/SkillExecution "{id: -}"
```

This command will execute the recipes of the skillset that corresponds to the use-case that was selected when the R3M-APG Orchestrator was launched, in STEP 1. In this case, it will select the skill recipes in the apg/recipes/r3mcell_cu_22 folder, for the Cube Kitting use-case.

## STEP 3: R3M Use-Case Program Execution

You can execute the whole CubeKitting use-case sequence using the following command:
```sh
ros2 run r3m_apg apg_SEQUENCE.py sequence:=1-100-12-13-6-12-14-15-7-14-1-100-22-23-6-22-24-25-7-24-1-100-32-33-6-32-34-35-7-34-1-100-42-43-6-42-44-45-7-44-1-100
```

## EXTRA: RL-Trained Agent Execution

TBD.

## EXTRA: R3M Perception for Object Pose Estimation

TBD.