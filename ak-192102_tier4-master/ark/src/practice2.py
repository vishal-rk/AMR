#!/usr/bin/python

import rospy
from goal_publisher.msg import PointArray
from move_base_msgs.msg import MoveBaseAction, MoveBaseGoal
from geometry_msgs.msg import PoseWithCovarianceStamped
from actionlib_msgs.msg import GoalStatus
import math 
import actionlib

class final(object):
	
	def __init__(self):
		#Initializing the node and variables
		rospy.init_node('Goalachievers')
		self.goalx=list()
		self.goaly=list()
		self.reward=list()
		self.cur_x=0;
		self.cur_y=0;

		# subscribing to the topics /goals /amcl_pose
		rospy.Subscriber("/goals", PointArray, self.point)
		rospy.Subscriber("amcl_pose", PoseWithCovarianceStamped, self.CurrentPosition)
		self.client = actionlib.SimpleActionClient('move_base',MoveBaseAction)
		self.client.wait_for_server()			
		rospy.sleep(1)

	# Current position for Robot
	def CurrentPosition(self,msg):
		self.cur_x=msg.pose.pose.position.x
		self.cur_y=msg.pose.pose.position.y


	#Storing Goal point received from AMR GOAL PUBLISHER
	def point(self,goals):
		self.goals=goals
		for i in range(0, len(self.goals.goals)):
			self.goalx.append(self.goals.goals[i].x)
			self.goaly.append(self.goals.goals[i].y)
			self.reward.append(self.goals.goals[i].reward)

	def goal_points(self,x,y):

		self.goal = MoveBaseGoal()
		self.goal.target_pose.header.frame_id = "map"
		self.goal.target_pose.header.stamp = rospy.Time.now()
	       
		# Points specifying the goal position coordinates
		self.goal.target_pose.pose.position.x = x
		self.goal.target_pose.pose.position.y = y
		self.goal.target_pose.pose.position.z = 0.0

	   # No rotation of the mobile base frame w.r.t. map frame
		self.goal.target_pose.pose.orientation.x = 0.0
		self.goal.target_pose.pose.orientation.y = 0.0
		self.goal.target_pose.pose.orientation.z = 0.0
		self.goal.target_pose.pose.orientation.w = 1.0

	   # Sends the goal to the action server.
		self.client.send_goal(self.goal)
	       
		# Waits for the server to finish performing the action.
		wait = self.client.wait_for_result()



	def ToGo(self):
		j=0
		Reward =0;
		#Assigning the goals based on Rewards with lowest reward first.
		for l in range(0,len(self.goals.goals)-1):
			for m in range(0,len(self.goals.goals)-l-1):
				if self.reward[m]>self.reward[m+1]:
					self.reward[m],self.reward[m+1] = self.reward[m+1],self.reward[m]
					self.goalx[m],self.goalx[m+1] = self.goalx[m+1],self.goalx[m]
					self.goaly[m],self.goaly[m+1] = self.goaly[m+1],self.goaly[m]
				
		#Send goal points to Move Base Package
		while j < len(self.goals.goals):
			self.goal_points(self.goalx[j],self.goaly[j])
			Reward =self.reward[j]
			rospy.loginfo("MOving towards reward = "+str(Reward ))
			j = j + 1
			rospy.sleep(1)
				
if __name__ == '__main__':
	pub=final()
	pub.ToGo()

