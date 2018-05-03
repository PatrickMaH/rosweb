#!/usr/bin/env python
import rospy
from std_msgs.msg import String
from geometry_msgs.msg import Twist

def mvcb(data):
	global msg

	if data.data == "forward":
		rospy.loginfo("receive forward")
		msg.linear.x = speed
		msg.angular.z = 0
	elif data.data == "back":
		rospy.loginfo("receive back")
		msg.linear.x = -speed
		msg.angular.z = 0
	elif data.data == "left":
		rospy.loginfo("receive left")
		if msg.linear.x != 0:
			if msg.angular.z < speed:
				msg.angular.z += 0.10
		else:
			msg.angular.z = speed *2
	elif data.data == "right":
		rospy.loginfo("receive right")
		if msg.linear.x != 0:
			if msg.angular.z > -speed:
				msg.angular.z -= 0.10
		else:
			msg.angular.z = -speed*2
	elif data.data == "stop":
		rospy.loginfo("receive stop")
		msg = Twist()

def miccb(data):
	if data.data == "mic":
		sub = rospy.Subscriber('/robot/recognizer/output', String, mvcb)
	else:
		sub.unregister()		

if __name__ == '__main__':
	speed = 0.2
	msg = Twist()
	rospy.init_node('robot_listener')

	rospy.Subscriber('to_robot_cmd', String, mvcb)	
	rospy.Subscriber('mic_label', String, miccb)

	pub = rospy.Publisher("/robot/mobile_base/commands/velocity", Twist, queue_size=10)
	r = rospy.Rate(2.0)
	while not rospy.is_shutdown():
		pub.publish(msg)
		r.sleep()
