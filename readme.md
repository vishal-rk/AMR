Team

@Amit Kushwaha
@Shubham Kadamdhad


**FINAL AMR PROJECT**

This repository contains following files:

1.readme file

2.ark package


**Prerequisites**

Launch the ak-192102_tier4 package.

**Description**

When the project is launched,The turtlebot  will navigate to as many different goal positions as possible
that are published on topic called /goals. We have used the movebase package which will use the map or arena 
to plan the trajectory of goal points. The move_base package provides an implementation of an action that, given a goal in the world, will attempt to reach it with a mobile base. The move_base node links together a global and local planner to accomplish its global navigation task


**Implementation**

The goal point subscribed from the topic /goals is stored in the empty list and sorted on the basis of lowest reward of the goal. After sorting the goals point list they are sent to the move base package which does the path planning using local and global cost map. when the one goal is achieved it takes the next goal from the list and robot starts move to next goal and so on.

**Problems**

The move_base package cannot reach a few points where the environment is full of obstacles and where the gap between the obstacle is about the width of the robot. It skips a goal point after trying all the recovery plans and then goes to the next goal point.

