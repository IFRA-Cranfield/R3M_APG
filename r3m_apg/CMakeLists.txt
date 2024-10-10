cmake_minimum_required(VERSION 3.8)
project(r3m_apg)

if(CMAKE_COMPILER_IS_GNUCXX OR CMAKE_CXX_COMPILER_ID MATCHES "Clang")
  add_compile_options(-Wall -Wextra -Wpedantic)
endif()

# find dependencies
find_package(ament_cmake REQUIRED)
# uncomment the following section in order to fill in
# further dependencies manually.
# find_package(<dependency> REQUIRED)

if(BUILD_TESTING)
  find_package(ament_lint_auto REQUIRED)
  # the following line skips the linter which checks for copyrights
  # comment the line when a copyright and license is added to all source files
  set(ament_cmake_copyright_FOUND TRUE)
  # the following line skips cpplint (only works in a git repo)
  # comment the line when this package is in a git repo and when
  # a copyright and license is added to all source files
  set(ament_cmake_cpplint_FOUND TRUE)
  ament_lint_auto_find_test_dependencies()
endif()

# =========================================================== #
# REQUIRED TO EXECUTE .py scripts:
install(
  DIRECTORY 
    skillexecution
    apg
  DESTINATION 
    share/${PROJECT_NAME}
)
install(PROGRAMS

  skillexecution/r3m_TRAIN.py
  skillexecution/r3m_EXECUTE.py
  
  skillexecution/wrappers/r3m_SkillExecution_Gazebo.py
  skillexecution/wrappers/r3m_SkillExecution_Gz_Perception.py
  skillexecution/wrappers/r3m_SkillExecution_RealRobot.py

  skillexecution/functions/ObjectState.py
  skillexecution/functions/CalculateRP.py
  skillexecution/functions/ResetGazebo.py
  skillexecution/functions/RestartGazebo.py
  skillexecution/functions/liaison.py
  skillexecution/functions/perception.py

  apg/apg_MATLAB.py
  apg/apg_SEQUENCE.py

  DESTINATION lib/${PROJECT_NAME} 
)

ament_package()