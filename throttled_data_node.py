#!/usr/bin/env python
from __future__ import print_function

import rospy
from sensor_msgs.msg import Image
from nav_msgs.msg import Odometry
import argparse

parser = argparse.ArgumentParser(description='Output data throttle node.')
parser.add_argument('rate', type=int, default=8, help='Sample rate in Hz')
args = parser.parse_args()

depth_img = None
rgb_img = None
odom = None

def depth_callback(data):
    global depth_img
    depth_img = data

def rgb_callback(data):
    global rgb_img
    rgb_img = data

def odom_callback(data):
    global odom
    odom = data


rospy.init_node('data_throttle_node')

rospy.Subscriber("/camera/depth/image_raw", Image, depth_callback)
depth_pub = rospy.Publisher('/camera/depth/image_raw_throttle_sync', Image, queue_size=10)
rospy.Subscriber("/camera/rgb/image_raw", Image, rgb_callback)
rgb_pub = rospy.Publisher('/camera/rgb/image_raw_throttle_sync', Image, queue_size=10)
rospy.Subscriber("/odom_combined", Odometry, odom_callback)
odom_pub = rospy.Publisher('/odom_combined_throttle_sync', Odometry, queue_size=10)

r = rospy.Rate(args.rate)
while not rospy.is_shutdown():
   r.sleep()
   if depth_img is not None and rgb_img is not None and odom is not None:
       depth_pub.publish(depth_img)
       rgb_pub.publish(rgb_img)
       odom_pub.publish(odom)
       depth_img = None
       rgb_img = None
       odom = None