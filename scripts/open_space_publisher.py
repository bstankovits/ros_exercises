#!/usr/bin/env python

import rospy
from sensor_msgs.msg import LaserScan
#from ros_exercises.msg import OpenSpace
from std_msgs.msg import Float32

#pub = rospy.Publisher(rospy.get_param('open_space/pub_topic', 'open_space'), OpenSpace, queue_size=20)
pub1 = rospy.Publisher(rospy.get_param('open_space/angle', 'open_space'), Float32, queue_size=20)
pub2 = rospy.Publisher(rospy.get_param('open_space/distance', 'open_space'), Float32, queue_size=20)

def callback(scan):
    longest_value = max(scan.ranges) 
    index_longest = scan.ranges.index(longest_value) 
    max_angle = scan.angle_min + index_longest*scan.angle_increment 

    pub1.publish(max_angle)
    pub2.publish(longest_value)
    
    # ospace = OpenSpace()
    # ospace.angle = max_angle
    # ospace.distance = longest_value
    # pub.publish(ospace)


def listen():
    rospy.init_node('open_space_publisher', anonymous = True)
    rate = rospy.Rate(20)
    rospy.Subscriber(rospy.get_param('open_space/sub_topic', 'fake_scan'), LaserScan, callback)
    rospy.spin() 


if __name__ == '__main__':
    try:
        listen()
    except rospy.ROSInterruptException:
        pass 