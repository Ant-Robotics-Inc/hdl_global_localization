#!/usr/bin/env python
# coding=utf8


"""
Ros node for control relocalization hdl slam method
"""

import re
from turtle import pos
import rospy
from sensor_msgs.msg import PointCloud2
from hdl_global_localization.srv import *
from geometry_msgs.msg import Pose
from std_srvs.srv import Trigger, TriggerResponse, TriggerRequest
import tf2_ros

global_cloud = None
local_cloud = None
offset_pose = Pose()
offset_pose.orientation.w = 1


def global_cloud_clb(data):
    global global_cloud
    global_cloud = data

def local_cloud_clb(data):
    global local_cloud
    local_cloud = data

def set_map_callback(data):
    rospy.wait_for_service('/hdl_global_localization/set_global_map')

    try:
        map_srv = rospy.ServiceProxy('/hdl_global_localization/set_global_map',  SetGlobalMap)
        resp = map_srv(data)
        return True
    except rospy.ServiceException, e:
        print ("Service call failed: %s"%e)
        return False

def set_fusion_map(data):
    rospy.wait_for_service('/hdl_global_localization/query')

    try:
        fusion_msg = rospy.ServiceProxy('/hdl_global_localization/query',  QueryGlobalLocalization)
        resp = fusion_msg(6,data)
        print("resp", resp.poses[0])
        return True, resp.poses[0]
    except rospy.ServiceException, e:
        print ("Service call failed: %s"%e)
        return False, None


def set_localisation(req):
    global offset_pose

    res = TriggerResponse()
    if (global_cloud == None or local_cloud == None):
        
        res.success = False
        res.message = "No points"
        return res
        
    if(set_map_callback(global_cloud)):
        print("set global map")
        state, offset_pose = set_fusion_map(local_cloud)

        if(state is False):
            res.success = False
            res.message = "Can't fount offset"
            return res

        res.success = True
        res.message = "Found offset!"+str(offset_pose)
        return res

    else:
        res.success = False
        res.message = "Global map can't init"
        return res
   

def set_tf_transform(event):
    global offset_pose
    if(offset_pose is None):
        print("offset_pose is None: EXIT")
        exit(0)
        
    static_transformStamped.header.stamp = rospy.Time.now()
    static_transformStamped.header.frame_id = "map"
    static_transformStamped.child_frame_id = "map_slam"

    static_transformStamped.transform.translation.x = offset_pose.position.x
    static_transformStamped.transform.translation.y = offset_pose.position.y
    static_transformStamped.transform.translation.z = offset_pose.position.z

    static_transformStamped.transform.rotation.x = offset_pose.orientation.x
    static_transformStamped.transform.rotation.y = offset_pose.orientation.y
    static_transformStamped.transform.rotation.z = offset_pose.orientation.z
    static_transformStamped.transform.rotation.w = offset_pose.orientation.w
    broadcaster.sendTransform(static_transformStamped)

if __name__ == '__main__':

    rospy.init_node('map_relocalization_node', anonymous=True)

    broadcaster = tf2_ros.StaticTransformBroadcaster()
    static_transformStamped = geometry_msgs.msg.TransformStamped()

    frame_id = "map" 
    child_id =  "map_slam"
    rate = 100.

    # init params
    frame_id = rospy.get_param("~frame_id", frame_id)
    child_id = rospy.get_param("~child_id", child_id)
    rate = rospy.get_param("~rate", rate)

    # init topics and service
    rospy.Subscriber("/global_map", PointCloud2, global_cloud_clb)
    rospy.Subscriber("/lio_sam/mapping/map_local", PointCloud2, local_cloud_clb)
    rospy.Timer(rospy.Duration(1./rate), set_tf_transform)
    s = rospy.Service('/relocalize', Trigger, set_localisation)

    rospy.spin()

  

