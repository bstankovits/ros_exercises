#!/usr/bin/env python

import rospy
import tf2_ros as tf2
import tf.transformations as tft 
from geometry_msgs.msg import TransformStamped
import numpy as np





if __name__ == '__main__':

    rospy.init_node('static_tf_cam_publisher')
    broadcast = tf2.StaticTransformBroadcaster()
    time = rospy.Time.now()
    
    _left_cam = TransformStamped()
    _left_cam.header.stamp = time
    _left_cam.header.frame_id = "base_link_gt"
    _left_cam.child_frame_id = "left_cam"

    _right_cam = TransformStamped()
    _right_cam.header.stamp = time
    _right_cam.child_frame_id = "right_cam"
    _right_cam.header.frame_id = "base_link_gt"
    

    left_trans_mat = np.array([[1, 0, 0, -.05],[0, 1, 0, 0], [0, 0, 1, 0], [0, 0, 0, 1]])

    _left_cam.transform.translation.x = left_trans_mat[0,3]
    _left_cam.transform.translation.y = left_trans_mat[1,3]
    _left_cam.transform.translation.z = left_trans_mat[2,3]

    right_trans_mat = np.array([[1, 0, 0, .05], [0, 1, 0, 0], [0, 0, 1, 0], [0, 0, 0, 1]])

    _right_cam.transform.translation.x = right_trans_mat[0,3]
    _right_cam.transform.translation.y = right_trans_mat[1,3]
    _right_cam.transform.translation.z = right_trans_mat[2,3]

    left_quat = tft.quaternion_from_matrix(left_trans_mat)

    _left_cam.transform.rotation.x = left_quat[0]
    _left_cam.transform.rotation.y = left_quat[1]
    _left_cam.transform.rotation.z = left_quat[2]
    _left_cam.transform.rotation.w = left_quat[3]

    right_quat = tft.quaternion_from_matrix(right_trans_mat)

    _right_cam.transform.rotation.x = right_quat[0]
    _right_cam.transform.rotation.y = right_quat[1]
    _right_cam.transform.rotation.z = right_quat[2]
    _right_cam.transform.rotation.w = right_quat[3]

    broadcast.sendTransform([_left_cam, _right_cam])
    rospy.spin()