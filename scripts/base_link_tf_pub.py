#!/usr/bin/env python

import rospy
import tf2_ros as tf2
import tf.transformations as tft 
from geometry_msgs.msg import TransformStamped
import numpy as np


def get_pose(transform, rotation):
    translation = transform.transform.translation
    translation_vec = [translation.x, translation.y, translation.z]
    translation_mat = tft.translation_matrix(translation_vec)

    rotation_mat = tft.quaternion_matrix([rotation.x, rotation.y, rotation.z, rotation.w])

    pose = tft.concatenate_matrices(translation_mat, rotation_mat)
    return pose


rospy.init_node('base_link_tf_pub', anonymous = True)
broadcast = tf2.TransformBroadcaster()


buffer = tf2.Buffer()
listener = tf2.TransformListener(buffer)

rate = rospy.Rate(10)


while not rospy.is_shutdown():
    try:
        world_to_left = buffer.lookup_transform("world", "left_cam", rospy.Time())
    except (tf2.LookupException, tf2.ConnectivityException, tf2.ExtrapolationException):
        rate.sleep()
        continue

    rotation = world_to_left.transform.rotation
    pose = get_pose(world_to_left, rotation)
  
    
    
