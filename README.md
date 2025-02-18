<div id="top"></div>

<!-- 

# ===================================== COPYRIGHT ===================================== #
#                                                                                       #
#                           ***** R3M Research Project *****                            #
#                                                                                       #
#  Reconfigurable Robotics for Responsive Manufacture (R3M) is a three-year research    #
#  project co-funded by the EPSRC and a group of Universities in the UK. The project    #
#  aims to develop new methods to enable the rapid and automated configuration of       #
#  robot manufacturing cells to allow mixed and variable products and processes to be   #
#  performed using the same basic hardware, the R3M Cell.                               #
#                                                                                       #
#  Licensed under the Apache-2.0 License.                                               #
#  You may not use this file except in compliance with the License.                     #
#  You may obtain a copy of the License at: http://www.apache.org/licenses/LICENSE-2.0  #
#                                                                                       #
#  Unless required by applicable law or agreed to in writing, software distributed      #
#  under the License is distributed on an "as-is" basis, without warranties or          #
#  conditions of any kind, either express or implied. See the License for the specific  #
#  language governing permissions and limitations under the License.                    #
#                                                                                       #
#  R3M Project Consortium:                                                              #
#                                                                                       #
#  AUTHORS (Cranfield University):                                                      #
#           Mikel Bueno Viso       - Mikel.Bueno-Viso@cranfield.ac.uk                   #
#           Dr. Seemal Asif        - s.asif@cranfield.ac.uk                             #
#           Prof. Phil Webb        - p.f.webb@cranfield.ac.uk                           #
#                                                                                       #
#  AUTHORS (Loughborough University):                                                   #
#           Dr. Paul Anandan       - p.d.anandan2@lboro.ac.uk                           #
#           Dr. Pedro Ferreira     - P.Ferreira@lboro.ac.uk                             #
#           Prof. Niels Lohse      - n.lohse@lboro.ac.uk                                #
#                                                                                       #
#  AUTHORS (Sheffield University):                                                      #
#           Yue Yao                - yue.yao@sheffield.ac.uk                            #
#           Dr. Ze Zhang           - ze.zhang@sheffield.ac.uk                           #
#           Dr. Windo Hutabarat    - w.hutabarat@sheffield.ac.uk                        #
#           Prof. Ashutosh Tiwari  - a.tiwari@sheffield.ac.uk                           #
#                                                                                       #
#  AUTHORS (AMRC - Sheffield):                                                          #
#           Dr. Gautham Ragunathan - g.ragunathan@amrc.co.uk                            #
#           Dr. Lloyd Tinkler      - l.tinkler@amrc.co.uk                               #
#                                                                                       #
#  Date: February, 2025.                                                                #
#                                                                                       #
# ===================================== COPYRIGHT ===================================== #

# ======= CITE OUR WORK ======= #
# You can cite our work with the following statement:
# R3M-APG (2025) Reconfigurable Robotics for Responsive Manufacture. URL: https://github.com/R3M-UK/R3M_APG.

-->

<!--

  README.md TEMPLATE obtined from:
      https://github.com/othneildrew/Best-README-Template
      AUTHOR: OTHNEIL DREW 

-->

<!-- HEADER -->
<br />

<div align="center">
  
  <a>
    <img src="media/EPSRC.png" alt="header" width="330" height="90">
  </a>

  <br />

  <h1 align="center">R3M-APG (Automated Program Generation)</h1>

  <h2 align="center">Reconfigurable Robotics for Responsive Manufacture</h2>

  <p align="center">
    R3M Research Project (United Kingdom)
    <br />
    Cranfield University - Loughborough University - Sheffield University - AMRC Sheffield
  </p>

  <a>
    <img src="media/R3MConsortium.png" alt="header" width="700" height="400">
  </a>

</div>
<br />

<!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#about">About</a>
      <ul>
        <li><a href="#r3m-research-project">R3M Research Project</a></li>
        <li><a href="#r3m-apg-repository">R3M-APG Repository</a></li>
        <li><a href="#ros2_simrealrobotcontrol-repository">ros2_SimRealRobotControl Repository</a></li>
      </ul>
    </li>
    <li><a href="#documentation">Documentation</a></li>
    <li><a href="#publications">Publications</a></li>
    <li><a href="#license">License</a></li>
    <li><a href="#cite-our-work">Cite our work</a></li>
    <li><a href="#contact">Contact</a></li>
  </ol>
</details>

<br />

<!-- ABOUT THE PROJECT -->
## About

### R3M Research Project

The R3M roject is dedicated to advancing adaptable and responsive manufacturing systems by leveraging cutting-edge robotics, AI, and automation. A key challenge in modern manufacturing is the inefficiency and high cost associated with reprogramming robotic systems to handle varying product demands. The R3M approach tackles this issue by developing algorithms capable of automatically generating configuration and programming data from product and process requirements, equipment specifications and CAD inputs, significantly reducing manual intervention.

ROS 2 has been the primary enabler for the reconfigurability and adaptability of the R3M system. By utilizing its modular architecture, real-time performance, and scalability, we have developed an automation framework that allows robotic systems to be dynamically reconfigured based on production demands. Through ROS 2’s distributed communication mechanisms, robotic cells can seamlessly integrate with external software and hardware components, ensuring interoperability across different manufacturers and setups. This integration is key to reducing downtime, improving efficiency, and enabling flexible automation, all of which are core objectives of the R3M Project.

The R3M Project is an EPSRC-funded UK research initiative (EP/V051180/1) focused on Reconfigurable Robotics for Responsive Manufacture. Led by Cranfield University, it is a collaborative effort involving Loughborough University, the University of Sheffield, and AMRC-Sheffield. Together, these institutions are working to develop next-generation, adaptable manufacturing systems that can dynamically respond to changing production needs while improving efficiency and reducing costs.

### R3M-APG Repository

Aa

### ros2_SimRealRobotControl Repository

The ros2_SimRealRobotControl repository has been developed as part of the R3M Project to address the challenges of reconfigurability and generalization in robotic arm programming and control. It provides a standardized framework that ensures modularity, interoperability, and seamless robot integration across different manufacturing setups. R3M-APG has been developed following the principles and architecture established in ros2_SimRealRobotControl, ensuring that robotic cells at Cranfield University and AMRC-Sheffield can be easily simulated, configured, and adapted for different tasks. By leveraging the modular design of ros2_SimRealRobotControl, R3M-APG benefits from predefined robot configurations, streamlined motion planning, and simplified deployment, making it a key component in the broader R3M initiative to enable flexible and responsive manufacturing systems.

The IFRA-Cranfield/ros2_SimRealRobotControl GitHub repository is a comprehensive framework designed to facilitate seamless integration of robots into both simulated and real-world environments using ROS 2. It provides a modular setup that allows for the easy deployment of various robot configurations, along with their corresponding controllers and end-effectors, without needing to redefine core parameters. The repository is built to support multiple robots, such as the ABB IRB-120, by enabling the use of ROS 2 packages that handle simulation, control, and MoveIt!2 for robot motion planning.

This repository is ideal for robotics researchers and developers who want to streamline the process of setting up robot environments for simulation and real-world tasks. It supports both Gazebo-based simulation for testing robot setups and MoveIt!2 for controlling robots in either virtual or physical environments. By organizing key robot and end-effector parameters in a modular way, it offers a flexible approach that makes it easy to switch between different robots, configurations, or tasks, accelerating both development and testing processes in industrial automation, robotics research, and advanced manufacturing systems.

Link to ros2_SimRealRobotControl: https://github.com/IFRA-Cranfield/ros2_SimRealRobotControl

<p align="right">(<a href="#top">back to top</a>)</p>

<!-- DOCUMENTATION -->
## Documentation

For detailed information on installation, usage, and requirements, please refer to the following documentation files available in this repository:

- [Installation.md](TBD): Instructions for setting up and installing the required dependencies.
- TBD

<p align="right">(<a href="#top">back to top</a>)</p>

<!-- PUBLICATIONS -->
## Academic Publications

Journal Papers:

- S. Asif, M. Bueno et al., “[Rapid and Automated Configuration of Robot Manufacturing Cells](https://www.sciencedirect.com/science/article/pii/S0736584524001492?via%3Dihub),” Robotics and Computer Integrated Manufacturing, vol. 92, p. 102862, Apr. 2025, doi: 10.1016/j.rcim.2024.102862.

Conference Papers:

- M. Bueno, I. Bernardino, S. Asif, and P. Webb, “[Unlocking the Potential of Robot Manipulators: Seamless Integration Framework](https://ieeexplore.ieee.org/document/10711476),” IEEE International Conference on Automation Science and Engineering, pp. 2610–2617, 2024, doi: 10.1109/CASE59546.2024.10711476.

- M. Bueno, J. Huang, S. Asif, F. Khan, and P. Webb, “[Towards Robot Software Abstraction: ROS 2-Based Framework for Object Handling within a Robot Cell](https://ieeexplore.ieee.org/document/10774307),” 2024 IEEE 22nd International Conference on Industrial Informatics (INDIN), pp. 1–8, Aug. 2024, doi: 10.1109/INDIN58382.2024.10774307.

<p align="right">(<a href="#top">back to top</a>)</p>

<!-- LICENSE -->
## License

<p>
  R3M Project Consortium (UK)
  <br />
  Main Investigator: Prof. Phil Webb (Cranfield University)
  <br />
  Main Contact: Dr. Seemal Asif (e-mail: s.asif@cranfield.ac.uk) 
  <br />
  <br />
  Licensed under the Apache-2.0 License.
  <br />
  You may obtain a copy of the License at: http://www.apache.org/licenses/LICENSE-2.0
  <br />
  <br />
  <a href="https://www.cranfield.ac.uk/">Cranfield University</a>
  <br />
  Faculty of Engineering and Applied Sciences (FEAS)
  <br />
    <a href="https://www.cranfield.ac.uk/centres/centre-for-robotics-and-assembly">Centre for Robotics and Assembly</a>
  <br />
  College Road, Cranfield
  <br />
  MK43 0AL, Bedfordshire, UK
  <br />
</p>

<p align="right">(<a href="#top">back to top</a>)</p>

<!-- CITE OUR WORK -->
## Cite our work

<p>
  You can cite our work with the following statement:
  <br />
  R3M-APG (2025) Reconfigurable Robotics for Responsive Manufacture. URL: https://github.com/R3M-UK/R3M_APG.
</p>

<p align="right">(<a href="#top">back to top</a>)</p>

<!-- CONTACT -->
## Contact

<p>

  CRANFIELD UNIVERSITY:
  <br />
  <br />
  Mikel Bueno Viso - Research Assistant in Intelligent Automation at Cranfield University
  <br />
  E-mail: Mikel.Bueno-Viso@cranfield.ac.uk
  <br />
  LinkedIn: https://www.linkedin.com/in/mikel-bueno-viso/
  <br />
  Profile: https://www.cranfield.ac.uk/people/mikel-bueno-viso-32884399
  <br />
  <br />
  Dr. Seemal Asif - Lecturer in Artificial Intelligence and Robotics at Cranfield University
  <br />
  E-mail: s.asif@cranfield.ac.uk
  <br />
  LinkedIn: https://www.linkedin.com/in/dr-seemal-asif-ceng-fhea-miet-9370515a/
  <br />
  Profile: https://www.cranfield.ac.uk/people/dr-seemal-asif-695915
  <br />
  <br />
  Professor Phil Webb - Professor of Aero-Structure Design and Assembly at Cranfield University
  <br />
  E-mail: p.f.webb@cranfield.ac.uk
  <br />
  LinkedIn: https://www.linkedin.com/in/phil-webb-64283223/
  <br />
  Profile: https://www.cranfield.ac.uk/people/professor-phil-webb-746415 
  <br />
  <br />

  LOUGHBOROUGH UNIVERSITY:
  <br />
  <br />
  Dr. Paul Anandan - Research Associate in Contextual Robot Programming
  <br />
  E-mail: p.d.anandan2@lboro.ac.uk
  <br />
  LinkedIn: https://www.linkedin.com/in/paul-danny-anandan-aa179257/
  <br />
  Profile: https://www.lboro.ac.uk/schools/meme/staff/paul-anandan/
  <br />
  <br />
  Dr. Pedro Ferreira - Senior Lecturer in Manufacturing Systems
  <br />
  E-mail: P.Ferreira@lboro.ac.uk
  <br />
  LinkedIn: https://www.linkedin.com/in/pedro-ferreira-0039279/
  <br />
  Profile: https://www.lboro.ac.uk/schools/meme/staff/pedro-ferreira/
  <br />
  <br />
  Professor Niels Lohse - Professor of Manufacturing Automation and Robotics
  <br />
  E-mail: n.lohse@lboro.ac.uk
  <br />
  LinkedIn: https://www.linkedin.com/in/niels-lohse-575b703/
  <br />
  Profile: https://www.lboro.ac.uk/schools/meme/staff/niels-lohse/
  <br />
  <br />

  SHEFFIELD UNIVERSITY:
  <br />
  <br />
  Yue Yao - Research Assistant in Robotics and Sensing for Manufacturing
  <br />
  E-mail: Yue.Yao@sheffield.ac.uk
  <br />
  LinkedIn: https://www.linkedin.com/in/alex-yue-yao/
  <br />
  Profile: https://www.sheffield.ac.uk/mac/people/research-staff/yue-yao
  <br />
  <br />
  Dr. Ze Zhang - Research Associate in Multi–Modal Sensing and Control for Responsive Manufacture
  <br />
  E-mail: ze.zhang@sheffield.ac.uk
  <br />
  LinkedIn: https://www.linkedin.com/in/ze-zhang-781306259/
  <br />
  Profile: https://www.sheffield.ac.uk/mac/people/research-staff/ze-zhang
  <br />
  <br />
  Dr. Windo Hutabarat - Research Associate in Digitisation of Manufacturing Processes
  <br />
  E-mail: w.hutabarat@sheffield.ac.uk
  <br />
  LinkedIn: https://www.linkedin.com/in/windohutabarat/
  <br />
  Profile: https://www.sheffield.ac.uk/mac/people/research-staff/windo-hutabarat
  <br />
  <br />
  Professor Ashutosh Tiwari - Deputy Vice-President for Innovation at the University of Sheffield
  <br />
  E-mail: a.tiwari@sheffield.ac.uk
  <br />
  LinkedIn: https://www.linkedin.com/in/ashutosh-tiwari-sheffield/
  <br />
  Profile: https://www.sheffield.ac.uk/mac/people/mech-eng-academic-staff/ashutosh-tiwari
  <br />
  <br />

  AMRC-SHEFFIELD:
  <br />
  <br />
  Dr. Gaugham Ragunathan - Postdoctoral Researcher (AMRC)
  <br />
  E-mail: g.ragunathan@amrc.co.uk 
  <br />
  LinkedIn: https://www.linkedin.com/in/gauthamragunathan/
  <br />
  Profile: --
  <br />
  <br />
  Dr. Lloyd Tinkler - Senior Technical Fellow, Electrical Materials (AMRC)
  <br />
  E-mail: l.tinkler@sheffield.ac.uk
  <br />
  LinkedIn: https://www.linkedin.com/in/lloyd-tinkler-72885620/
  <br />
  Profile: https://www.sheffield.ac.uk/amrc/amrc-research-staff/lloyd-tinkler
  <br />
  <br />

</p>

<p align="right">(<a href="#top">back to top</a>)</p>