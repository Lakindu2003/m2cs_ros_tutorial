#!/usr/bin/env python
import rospy
from math import pi, fmod, sin, cos, sqrt
from geometry_msgs.msg import Twist
# hint: some imports are missing
from turtlesim.msg import Pose
from turtle_path.srv import *

cur_pos = Pose()

def cb_pose(data): # get the current position from subscribing the turtle position
    global cur_pos
    cur_pos = data
    
def cb_walk(req):
    if (req.distance < 0):
        return False
    
    # hint: calculate the projected (x, y) after walking the distance,
    # and return false if it is outside the boundary
    x = ( cos(cur_pos.theta) * req.distance) + cur_pos.x
    y = ( sin(cur_pos.theta) * req.distance) + cur_pos.y
    if x > 11 or x < 0 or y < 0 or y > 11:
        return False
        
    rate = rospy.Rate(100) # 100Hz control loop
    rem_dist = sqrt((x-cur_pos.x)**2 + (y-cur_pos.y)**2)
    vel = Twist()
    t = 100
    vel.linear.x = x/t
    vel.linear.y = y/t

    while (rem_dist <= 0.05): # control loop
        
        # in each iteration of the control loop, publish a velocity

        # hint: you need to use the formula for distance between two points
        #rem_dist = sqrt((x-cur_pos.x)**2 + (y-cur_pos.y)**2)
        rem_dist = sqrt((x-cur_pos.x)**2 + (y-cur_pos.y)**2)
        pub.publish(vel)
        
        rate.sleep()
        
    
    # publish a velocity 0 at the end, to ensure the turtle really stops
    vel.linear.x = 0.0; vel.linear.y = 0.0
    pub.publish(vel)

    return True

def cb_orientation(req):

    rate = rospy.Rate(100) # 100Hz control loop
    dist = fmod(req.orientation - cur_pos.theta + pi + 2 * pi, 2 * pi) - pi
    vel = Twist() 
    vel.angular.z = dist/100
    
    while (dist <= 0.05): # control loop
        
        # in each iteration of the control loop, publish a velocity

        # hint: signed smallest distance between two angles: 
        # see https://stackoverflow.com/questions/1878907/the-smallest-difference-between-2-angles
        dist = fmod(req.orientation - cur_pos.theta + pi + 2 * pi, 2 * pi) - pi
        pub.publish(vel)

        rate.sleep()
    
    # publish a velocity 0 at the end, to ensure the turtle really stops
    vel.angular.z = 0.0
    pub.publish(vel)

    return True

if __name__ == '__main__':
    rospy.init_node('path_manager')
    
    pub = rospy.Publisher("velocity", Twist, queue_size = 1) # publisher of the turtle velocity
    sub = rospy.Subscriber("position", Pose, cb_pose) # subscriber of the turtle position, callback to cb_pose
    
    ## init each service server here:
    srv_ori = rospy.Service("orientation", SetOrientation, cb_orientation)		# callback to cb_orientation
    srv_walk_dis = rospy.Service("Distance", WalkDistance, cb_walk)		# callback to cb_walk
    
    rospy.spin()
    