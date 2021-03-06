#!/usr/bin/env python


import roslib; roslib.load_manifest('pocketsphinx')
import rospy
import math

from geometry_msgs.msg import Twist
from std_msgs.msg import String

class voice_cmd_vel:

    def __init__(self):
        rospy.on_shutdown(self.cleanup)
        self.speed = 0.2
        self.msg = Twist()
        self.mic_label = "mic"

        # publish to cmd_vel, subscribe to speech output
        rospy.Subscriber('mic_label', String, self.micCb)
        self.pub = rospy.Publisher('/robot/mobile_base/commands/velocity', Twist, queue_size=10)
        rospy.Subscriber('recognizer/output', String, self.speechCb)

        r = rospy.Rate(10.0)
        while not rospy.is_shutdown():
            if self.mic_label == "mic":
                rospy.loginfo("=== mic ===") 
                self.pub.publish(self.msg)
            r.sleep()
        
    def micCb(self, msg):
        self.mic_label = msg.data
        rospy.loginfo("self.mic_label: %s", msg.data)

    def speechCb(self, msg):
        rospy.loginfo(msg.data)
        
        if msg.data.find("forward") > -1: 
            rospy.loginfo("=== input: forward ===")   
            self.msg.linear.x = self.speed
            self.msg.angular.z = 0
        elif msg.data.find("left") > -1:
            rospy.loginfo("=== input: left ===") 
            if self.msg.linear.x != 0:
                if self.msg.angular.z < self.speed:
                    self.msg.angular.z += 0.05
            else:        
                self.msg.angular.z = self.speed*2
        elif msg.data.find("right") > -1: 
            rospy.loginfo("=== input: right ===")    
            if self.msg.linear.x != 0:
                if self.msg.angular.z > -self.speed:
                    self.msg.angular.z -= 0.05
            else:        
                self.msg.angular.z = -self.speed*2
        elif msg.data.find("back") > -1:
            rospy.loginfo("=== input: back ===") 
            self.msg.linear.x = -self.speed
            self.msg.angular.z = 0
        elif msg.data.find("stop") > -1:
            rospy.loginfo("=== input: stop ===")           
            self.msg = Twist()
        

    def cleanup(self):
        # stop the robot!
        twist = Twist()
        self.pub.publish(twist)

if __name__=="__main__":
    rospy.init_node('voice_cmd_vel')
    try:
        voice_cmd_vel()
    except:
        pass

