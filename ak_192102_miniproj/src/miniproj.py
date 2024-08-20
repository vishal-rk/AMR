#! /usr/bin/env python
import rospy
from tf.transformations import euler_from_quaternion
import tf
import math
from math import atan2
from geometry_msgs.msg import Twist
from gazebo_msgs.msg import ModelStates
from sensor_msgs.msg import LaserScan
from goal_publisher.msg import PointArray

class robot(object):

	def __init__(self):

		rospy.init_node('dest_publisher')
		self.x=0
		self.y=0
		self.curryaw=0
		self.front=[0]*10
		self.left=[0]*10
		self.right=[0]*10
		self.goalx=[0]*20
		self.goaly=[0]*20
		self.goalxt=[0]*20
		self.goalyt=[0]*20
		self.min_front=0
		self.min_left=0
		self.min_right=0
		self.dfo = [0]*20

		self.pub=rospy.Publisher("cmd_vel", Twist, queue_size=1)
		rospy.Subscriber("/goals", PointArray, self.point)
		rospy.Subscriber("/gazebo/model_states", ModelStates, self.position)
		rospy.Subscriber("/scan", LaserScan, self.scanner)
		rospy.sleep(3)
	
	def position(self,msg):
		self.x=msg.pose[1].position.x 
		self.y=msg.pose[1].position.y
		rot=msg.pose[1].orientation
		(r, p, self.curryaw) = tf.transformations.euler_from_quaternion([rot.x, rot.y, rot.z, rot.w])

	def point(self,pnt):
		for j in range(20):
			self.goalx[j]=pnt.goals[j].x
			self.goaly[j]=pnt.goals[j].y
		
	def scanner(self,msg):
		 
		self.front[5:]=msg.ranges[354:]
		self.front[:5]=msg.ranges[0:5]
		self.left[:]=msg.ranges[50:60]
		self.right[:]=msg.ranges[310:320]
		self.min_front=min(self.front)
		self.min_left=min(self.left)
		self.min_right=min(self.right)

	def distance(self,x1,y1,x2,y2):
		
		d=math.sqrt((x2-x1)**2+(y2-y1)**2)
		return d

	def angular(self,tx,ty):
		
		inc_x=tx-self.x
		inc_y=ty-self.y
		theta=atan2(inc_y,inc_x)	
		return theta
		
	def destination(self):

		vel=Twist()
		r=rospy.Rate(5)
				
		for i in range (20):
					
			for s in range(20):		
				self.goalxt[s] = self.goalx[s]
			
			for t in range(20):		
				self.goalyt[t] = self.goaly[t]
			
			for k in range(20):		
				self.dfo[k] = self.distance(0,0,self.goalxt[k],self.goalyt[k])
		
			
			for l in range(20):
			 
				for m in range(0,20-l-1):
					if self.dfo[m]>self.dfo[m+1]:
						self.dfo[m],self.dfo[m+1] = self.dfo[m+1],self.dfo[m]
						self.goalxt[m],self.goalxt[m+1] = self.goalxt[m+1],self.goalxt[m]
						self.goalyt[m],self.goalyt[m+1] = self.goalyt[m+1],self.goalyt[m]	
					
			for g in range(20):
				if self.goalxt[i]==self.goalx[g] and self.goalyt[i]==self.goaly[g]:
					ans=g
																																																										
			while (self.distance(self.x,self.y,self.goalxt[i],self.goalyt[i])>=0.3):
											
				angle=self.angular(self.goalxt[i],self.goalyt[i])
				
				
				if self.min_front >= 0.5 and self.min_left >= 0.5 and self.min_right >= 0.5:  
					rospy.loginfo("Moving forward toward goal %d",ans+1)		
									
					if abs(angle-self.curryaw)>0.1 :
						vel.linear.x=0
						vel.angular.z=0.2
						self.pub.publish(vel)
						r.sleep()	
					else:
						vel.angular.z=0
						vel.linear.x=0.3
						self.pub.publish(vel)
						r.sleep()

				elif self.min_front >= 0.5 and self.min_left < 0.5 and self.min_right < 0.5 :
					rospy.loginfo("Object detected in left and right")				
								
					if abs(angle-self.curryaw)>0.1 :
						vel.linear.x=0
						vel.angular.z=0.2
						self.pub.publish(vel)
						r.sleep()	
					else:
						vel.angular.z=0
						vel.linear.x=0.3
						self.pub.publish(vel)
						r.sleep()

				elif self.min_front >= 0.5 and self.min_left < 0.5 and self.min_right >= 0.5 :
					rospy.loginfo("Object detected in left ")				
					vel.angular.z = -0.2
					vel.linear.x = 0.3
					self.pub.publish(vel)
					r.sleep()				
							
				elif self.min_front >= 0.5 and self.min_left >= 0.5 and self.min_right < 0.5 :
					rospy.loginfo("Object detected in right")						
					vel.angular.z = 0.2
					vel.linear.x = 0.3
					self.pub.publish(vel)
					r.sleep()				
								               			
				elif self.min_front < 0.5 and self.min_left >= 0.5 and self.min_right >= 0.5 :
					rospy.loginfo("Object detected in front ")				
					vel.linear.x=-0.2			
					vel.angular.z=-0.2				
					self.pub.publish(vel)
				 	r.sleep()
						
				elif self.min_front < 0.5 and self.min_left < 0.5 and self.min_right >= 0.5 :
					rospy.loginfo("Object detected in left and front")				
					vel.linear.x=-0.3			
					vel.angular.z=-0.2				
					self.pub.publish(vel)
					r.sleep()

				elif self.min_front < 0.5 and self.min_left >= 0.5 and self.min_right < 0.5 :
					rospy.loginfo("Object detected in front and right")				
					vel.linear.x=-0.3			
					vel.angular.z=0.2				
					self.pub.publish(vel)
					r.sleep()

				else:
					rospy.loginfo("Object detected in left, front and right")
					vel.linear.x=-0.3			
					vel.angular.z=-0.2				
					self.pub.publish(vel)
					r.sleep()

			if(self.distance(self.x,self.y,self.goalxt[i],self.goalyt[i])<=0.3):
				vel.linear.x=0
				vel.angular.z=0
				self.pub.publish(vel)
				r.sleep()
		        	rospy.loginfo("Reached goal %d ",ans+1)
			
if __name__ == '__main__':
    pub = robot()
    pub.destination()


