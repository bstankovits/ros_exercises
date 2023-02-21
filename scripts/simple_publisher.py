#!/usr/bin/env python
# license removed for brevity

import rospy
from std_msgs.msg import Float32
import random

#Publishes a random number between 0 and 10.
def simple_publisher():
	pub = rospy.Publisher('my_random_float', Float32, queue_size = 10)
	rospy.init_node('simple_publisher', anonymous = True)
	rate = rospy.Rate(20)
	while not rospy.is_shutdown():
		num = random.uniform(0.0, 10.0)
		rospy.loginfo(num)
		pub.publish(num)
		rate.sleep()





if __name__ == '__main__':
	try:
		simple_publisher()
	except rospy.ROSInterruptException:
		pass
