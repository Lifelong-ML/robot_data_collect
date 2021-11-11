#! /usr/bin/env python
import rospy
from geometry_msgs.msg import Twist
from sensor_msgs.msg import Joy
from sensor_msgs.msg import Image
import subprocess
import os
from cv_bridge import CvBridge, CvBridgeError
# OpenCV2 for saving an image
import cv2
import time
#/camera/rgb/image_raw

# This ROS Node converts Joystick inputs from the joy node
# into commands for turtlesim or any other robot

# Receives joystick messages (subscribed to Joy topic)
# then converts the joysick inputs into Twist commands
# axis 1 aka left stick vertical controls linear speed
# axis 0 aka left stick horizonal controls angular speed

debounce = [False] * 22
bridge = CvBridge()
img_msg = None
img_save_idx = 0

def button_down(idx, data):
    if data.axes[idx] < 0:
        if not debounce[idx]:
            debounce[idx] = True
	    return True
    else:
        debounce[idx] = False
    return False

def save_latest_rgb():
    global img_save_idx
    if img_msg is None:
	print("No image to save")
        return
    try:
        # Convert your ROS Image message to OpenCV2
        cv2_img = bridge.imgmsg_to_cv2(img_msg, "bgr8")
    except CvBridgeError, e:
        print(e)
    else:
        # Save your OpenCV2 image as a jpeg
        cv2.imwrite('/data/robot_collection/individual_images/camera_image%f.jpg' % time.time(), cv2_img)
        img_save_idx += 1


def rgb_callback(msg):
    global img_msg 
    img_msg = msg

def callback(data):
    #twist = Twist()
    #print(list(enumerate(data.axes)))

    if button_down(18, data):
        print("Picture")
        save_latest_rgb()
    if button_down(17, data):
        print("Talk")
        os.system('say "Hello meat bag"')

    #twist.linear.x = 4*data.axes[7]
    #twist.angular.z = 4*data.axes[6]
    #pub.publish(twist)


# Intializes everything
def start():
    # publishing to "turtle1/cmd_vel" to control turtle1
    global pub
    #pub = rospy.Publisher('turtle1/cmd_vel', Twist)
    # subscribed to joystick inputs on topic "joy"
    rospy.Subscriber("joy", Joy, callback, queue_size=3)
    rospy.Subscriber("/camera/rgb/image_raw", Image, rgb_callback, queue_size=1)
    # starts the node
    rospy.init_node('Joy2Turtle')
    rospy.spin()

if __name__ == '__main__':
    start()
