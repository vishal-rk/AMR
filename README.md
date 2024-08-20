**AMR MINIPROJECT**

This repository contains follows:
1. ak_192192_miniproj
2. mini_project_master
3. readme file

**Setup**

1. run the roscore
2. Launch the turtlebot3 empty world package
3. run rosrun gazebo_ros spawn_model
4. Launch the start.launch(which include the goal_publisher_package)

**Description**

The goal of this mini project is when launched it will navigate the turtlebot to different goal positions as possible provided in the goal_publisher_package using the laserscan data obtained to navigate through obstacle present to reach goals. The current position of the robot is obtained from /gazebo/model_states. 

**Algorithm**

In starting the sorting of goals is done to obtain the shortest golal possible. The main idea is to first reach the shortest goal present and then navigate to next shortest second goal ans so on. once the goals are sorted the robot start moving towards it, using def scanner( ) function it scan the front, left, right and take min_front, min_left and min_right. if the there is no obstacle present in front of the robot of .5 m it will move in the correct path if the there is obstacle it will change the path using the destination() function in which 8 conditions are provided for the robot to decide in which direction to move to avoid obstacles. If the robot distance between the robot is less than or equall to 0.3m it stops and start moving to next shortest goal from that point.

