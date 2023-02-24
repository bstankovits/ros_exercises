#!/usr/bin/env python

import rospy
import tf2_ros as tf2
import tf.transformations as tft 
from geometry_msgs.msg import TransformStamped
import numpy as np


rospy.init_node('dynamic_tf_cam_publisher', anonymous=True)

broadcaster = tf2.TransformBroadcaster()
tfBuffer = tf2.Buffer()
tflistener = tf2.TransformListener(tfBuffer)
rate = rospy.Rate(10)


def get_pose(robot_trans, rotation):
    translation = robot_trans.transform.translation
    
    trans_vec = [translation.x, translation.y, translation.z]
    rotation_vec = [rotation.x, rotation.y, rotation.z, rotation.w]

    translMat = tft.translation_matrix(trans_vec)
    rotMat = tft.quaternion_matrix(rotation_vec)
    pose = tft.concatenate_matrices(translMat, rotMat)
    return pose


while not rospy.is_shutdown():
    try:
        robot_trans = tfBuffer.lookup_transform("world", "base_link_gt", rospy.Time())
    except (tf2.ConnectivityException, tf2.ExtrapolationException, tf2.LookupException):
        rate.sleep()
        continue
    rotation = robot_trans.transform.rotation 
    pose = get_pose(robot_trans, rotation)
    
    left_cam_to_bl = tft.translation_matrix([-0.05, 0, 0])
    left_cam_to_world = tft.concatenate_matrices(pose, left_cam_to_bl)
    right_cam_to_left_cam = tft.translation_matrix([0.1, 0, 0])
    
    _left_cam = TransformStamped()

    _left_cam.header.stamp = rospy.Time.now()
    _left_cam.header.frame_id = 'world'
    _left_cam.child_frame_id = 'left_cam'

    left_cam_world_vec = tft.translation_from_matrix(left_cam_to_world)
    _left_cam.transform.translation.x = left_cam_world_vec[0]
    _left_cam.transform.translation.y = left_cam_world_vec[1]
    _left_cam.transform.translation.z = left_cam_world_vec[2]
    
    _left_cam.transform.rotation.x = rotation.x
    _left_cam.transform.rotation.y = rotation.y
    _left_cam.transform.rotation.z = rotation.z
    _left_cam.transform.rotation.w = rotation.w

    _right_cam = TransformStamped()

    _right_cam.header.stamp = rospy.Time.now()
    _right_cam.header.frame_id = 'left_cam'
    _right_cam.child_frame_id = 'right_cam'

    right_cam_tvec = tft.translation_from_matrix(right_cam_to_left_cam)
    _right_cam.transform.translation.x = right_cam_tvec[0]
    _right_cam.transform.translation.y = right_cam_tvec[1]
    _right_cam.transform.translation.z = right_cam_tvec[2]
    
    right_cam_rvec = tft.quaternion_from_matrix(right_cam_to_left_cam)
    _right_cam.transform.rotation.x = right_cam_rvec[0]
    _right_cam.transform.rotation.y = right_cam_rvec[1]
    _right_cam.transform.rotation.z = right_cam_rvec[2]
    _right_cam.transform.rotation.w = right_cam_rvec[3]

    broadcaster.sendTransform([_left_cam, _right_cam])
    rate.sleep()