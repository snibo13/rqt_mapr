#!/usr/bin/env python3
import rospy
from std_msgs.msg import Int8

def callback(msg):
	data = msg.data
	if (data ==  1):
		os.system("roslaunch mapr mapr_gmapping_enc.launch")
	elif(data == 3):
		os.system("roslaunch mapr_nav mapr_nav.launch")
		# case 2:
			# os.system("roslaunch mapr mapr_gmapping_match.launch")
	elif(data == 4):
		os.system("roslaunch mapr mapr_amcl.launch")
	elif (data == 5):
		os.system("rosrun map_server map_saver -f map.pgm")


def listener():
    rospy.init_node('mission_control', anonymous=True)
    rospy.Subscriber("mission_command", Int8, callback)
    rospy.spin()

if __name__ == '__main__':
    listener()
