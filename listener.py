#!/usr/bin/env python3
import rospy
from std_msgs.msg import Int8

def callback(msg):
	match (msg.data):
		case 1:
			os.system("roslaunch mapr mapr_gmapping_enc.launch")
		case 3:
			os.system("roslaunch mapr_nav mapr_nav.launch")
		# case 2:
			# os.system("roslaunch mapr mapr_gmapping_match.launch")
		case 4:
			os.system("roslaunch mapr mapr_amcl.launch")
		case 5:
			os.system("rosrun map_server map_saver -f map.pgm")


def listener():
    rospy.init_node('mission_control', anonymous=True)
    rospy.Subscriber("mission_command", Int8, callback)
    rospy.spin()

if __name__ == '__main__':
    listener()