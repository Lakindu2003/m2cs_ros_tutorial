#!/usr/bin/env python
import rospy
from geometry_msgs.msg import Twist
from turtlesim.srv import SetPen
# hint: some imports are missing
from m2_ps4.msg import Ps4Data
from std_srvs.srv import Empty

old_data = Ps4Data()

def callback(data):
    global old_data
    k = 1
    # you should publish the velocity here!
    
    # hint: to detect a button being pressed, you can use the following pseudocode:
    # 
    # if ((data.button is pressed) and (old_data.button not pressed)),
    # then do something...
    if data.dpad_y > 0 and  old_data.dpad_y <= 0:
        k *= 2
    if data.dpad_y < 0 and  old_data.dpad_y >= 0:
        k /= 2
   # if (data.hat_ly == True and  old_data.hat_ly == False) or (data.hat_rx == True and  old_data.hat_rx == False):
   #     data.hat_ly *= k; data.hat_rx *= k
   #     pub.publish(data)
   #     old_data = data
    
    if (data.hat_ly == True and  old_data.hat_ly == False):
        vel = Twist()
        if data.hat_ly > 0: vel.linear.y = k
        else: vel.linear.y = -k
        pub.publish(vel)

    if (data.hat_rx == True and  old_data.hat_rx == False):
        vel = Twist()
        if data.hat_rx > 0: vel.linear.x = k
        else: vel.linear.x = -k
        pub.publish(vel)



    #clear
    if data.ps == True and old_data.ps == False:
        srv_clr_bg(Empty())

    #setpen
    if data.Triangle == True and old_data.triangle == False:
        req = SetPen()
        req.g = 255; req.b = 0; req.r = 0
        srv_col(req)

    if data.circle == True and old_data.circle == False:
        req = SetPen()
        req.g = 0; req.b = 0; req.r = 255
        srv_col(req)

    if data.cross == True and old_data.cross == False:
        req = SetPen()
        req.g = 0; req.b = 255; req.r = 0
        srv_col(req)

    if data.square == True and old_data.square == False:
        req = SetPen()
        req.g = 0; req.b = 255; req.r = 255
        srv_col(req)
    
    old_data = data
        
    


if __name__ == '__main__':
    rospy.init_node('ps4_controller')
    
    pub = rospy.Publisher("cmd_vel", Twist, queue_size = 1) # publisher object goes here... hint: the topic type is Twist
    sub = rospy.Subscriber("input/ps4_data", Ps4Data, callback) # subscriber object goes here
    
    # one service object is needed for each service called!
    srv_col = rospy.ServiceProxy("set_pen", SetPen) # service client object goes here... hint: the srv type is SetPen
    # fill in the other service client object...
    srv_clr_bg = rospy.ServiceProxy("clear", Empty)
    rospy.spin()

