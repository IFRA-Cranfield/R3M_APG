clear,clc

node = ros2node("R3M_SkillExecution_CLIENT")
client = ros2svcclient(node, "/r3m_SkillExecution", "r3mcell_data/SkillExecution")

waitForServer(client, "Timeout", 3);

request = ros2message(client)
request.id = int32(3)

response = call(client, request, "Timeout", 3)