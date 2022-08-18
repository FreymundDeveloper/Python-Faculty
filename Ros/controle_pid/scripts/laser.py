#!/usr/bin/env python

import rospy
from geometry_msgs.msg import Twist
from sensor_msgs.msg import LaserScan


ranged1= [5]
ranged2= [5]
ranged3= [5]

def callback(msg):
    global ranged1 
    global ranged2 
    global ranged3

    ranged1 = msg.ranges[0:169] #direito
    ranged2 = msg.ranges[170:339] #meio
    ranged3 = msg.ranges[340:511] #esquerdo
    

def publisher():
    rospy.init_node('stage_vrap_range', anonymous=True)
    pub = rospy.Publisher('/cmd_vel', Twist, queue_size=10)
    sub = rospy.Subscriber('/scan', LaserScan, callback)

    rate = rospy.Rate(10)
    msg = Twist()

    while True:
        msg.linear.x = 3
        msg.angular.z = 0

        min1 = min(ranged1)
        min2 = min(ranged2)
        min3 = min(ranged3)

        if min1 < 0.5 or min2 < 0.5 or min3 < 0.5:

            if min2 <0.3:
                msg.linear.x = 0.1

            elif min2 < 1:
                msg.linear.x = 0.5

            else:
                msg.linear.x = 2
            
            if min1 < 0.5 and min2 < 0.5:
                msg.angular.z = 6

            elif min3 < 0.5 and min2 < 0.5:
                msg.angular.z = -6

        elif min1 < 0.5:
            msg.linear.x = 0.5
            msg.angular.z = 4             

        elif min3 < 0.5:
            msg.linear.x = 0.5
            msg.angular.z = -4 


        pub.publish(msg)
        rate.sleep()
   

if __name__ == '__main__':
    try:
        publisher()
    except rospy.ROSInterruptException:
        pass