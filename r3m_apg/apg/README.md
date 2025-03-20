# R3M Research Project - R3M-APG (Automated Program Generation)

## Automated Program Generation (APG)

The /APG folder within the R3M-APG repository contains the core components responsible for managing and executing Automated Program Generation (APG) processes in the R3M-Cell. The APG system is designed to automate and streamline the execution of robot skills through predefined use-cases and recipes, while also supporting Reinforcement Learning (RL)-based execution for adaptive and optimised task performance. This folder contains the necessary configuration files, RL agents, and execution scripts that enable both manual and autonomous execution of robot programs.

## Key Sub-Directories

The folder is structured into several key sub-directories. The /usecase folder contains .yaml configuration files that define the parameters and specifications for each R3M use-case. These configurations include details such as the robot cell setup, robot skills required, and execution parameters. 

The /recipes folder stores the individual robot skill recipes, which are sequentially executed to perform a complete use-case. Each use-case has its own subfolder containing all the recipes necessary for its execution. 

The /agents folder holds the trained RL agents used for autonomous execution. These agents have been pre-trained using simulation-based RL techniques to optimise the performance of specific use-cases. 

Additionally, the /matlab folder includes example MATLAB .m and Simulink .slx files, which have been used to train RL agents using the R3M-Gazebo APG Training environment.

## apg_MATLAB.py: APG AGENT execution

The apg_MATLAB.py script enables agent-driven execution of R3M programs by loading a specified trained RL agent and running the corresponding use-case program. The script autonomously handles the execution sequence, allowing the RL agent to manage the robot skill recipes optimally based on its learned policy. This facilitates adaptive program execution, where the agent dynamically adjusts the robot’s behaviour based on its training, making the system more efficient and responsive in handling complex use-cases.

### Execution: Pre-requisites

Matlab (>= 2024a) and the MATLAB Engine API for Python must be installed in the Ubuntu 22.04 machine for this feature to work.

```sh
# MATLAB Installation (Ubuntu 22.04): https://uk.mathworks.com/help/install/ug/install-products-with-internet-connection.html
# MATLAB-Python engine: https://uk.mathworks.com/help/matlab/matlab_external/install-the-matlab-engine-for-python.html -> Once Matlab is installed, in the terminal, type: 
python -m pip install matlabengine
```

### Execution

(EXAMPLE) This command executes the RL Trained Agent node for the Cylinder Stacking use-case at the AMRC Cell (amrc_13 use-case). It loads the r3mcell_amrc_13.mat trained agent, which is stored in the /apg/agents folder:
```sh
ros2 run r3m_apg apg_MATLAB.py usecase:=r3mcell_amrc_13
```

## apg_SEQUENCE.py: APG STATIC SEQUENCE execution

The apg_SEQUENCE.py script offers a manual execution mode, allowing users to define and run a custom sequence of robot skill recipes. Unlike the RL-based execution, this script requires the user to directly specify the sequence of recipes by inputting their numbers in the terminal. This provides greater control and flexibility, making it ideal for testing, debugging, and fine-tuning specific use-cases in the R3M-Cell environment.

### Execution:

(EXAMPLE) This command executes the sequence of recipes (manually, without agent intervention) for the Cube Stacking use-case at the Cranfield University cell (cu_11 use-case):
```sh
ros2 run r3m_apg apg_SEQUENCE.py sequence:=1-100-2-3-6-2-4-5-7-4-1-100-12-13-6-12-14-15-7-14-1-100
```