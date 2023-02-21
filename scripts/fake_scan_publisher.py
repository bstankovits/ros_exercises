#!/usr/bin/env python 

import rospy
from sensor_msgs.msg import LaserScan
import random
import math 

def talker():
    pub = rospy.Publisher(rospy.get_param('fake_scan/pub_topic', '/fake_scan'), LaserScan, queue_size = 20)
    rospy.init_node('fake_scan_publisher', anonymous = True)
    rate = rospy.Rate(rospy.get_param('fake_scan/pub_rate', 20)) #20 hz

    while not rospy.is_shutdown():
        scan = LaserScan()
        scan.header.stamp = rospy.Time.now() 
        scan.header.frame_id = 'base_link'
        scan.angle_min = eval(rospy.get_param('fake_scan/angle_min', '(-2.0/3.0)*math.pi'))
        scan.angle_max = eval(rospy.get_param('fake_scan/angle_max', '(2.0/3.0)*math.pi'))
        scan.angle_increment = eval(rospy.get_param('fake_scan/angle_increment', '(1.0/300.0)*math.pi'))
        scan.scan_time = 1.0/rospy.get_param('fake_scan/pub_rate', 20)
        scan.range_min = rospy.get_param('fake_scan/range_min', 1.0)
        scan.range_max = rospy.get_param('fake_scan/range_max', 10.0)
        scan.ranges = []

        for i in range(int(round(abs((scan.angle_max - scan.angle_min)/scan.angle_increment))) + 1):
            scan.ranges.append(random.uniform(scan.range_min, scan.range_max))

        pub.publish(scan)
        rate.sleep()

if __name__ == '__main__':
    try:
        talker()
    except rospy.ROSInterruptException:
        pass