#!/usr/bin/env python
import rospy
from geometry_msgs.msg import Twist
from std_msgs.msg import Int16
from sensor_msgs.msg import Joy

tar_vel = 0
act_vel = 0
error_sum = 0
prev_error = 0
error_diff = 0
output = 0
kp = 0
ki = 0
kd = 0

def callback_joy(data):
    global tar_vel
    if data.buttons[3] :
        tar_vel += 1
    if data.buttons[0] :
        tar_vel -= 1
    if data.axes[5] < 1 :
        tar_vel = 0


def callback_can(data):
    global act_vel
    global tar_vel
    global error_sum
    global error
    global error_diff
    global output
    global i
    global flag
    global kp
    global ki
    global kd

    act_vel = data.data
    if act_vel==tar_vel and flag==1:
        i=0
        flag=0
    if flag==0:
        i+=1
        if i==100:
            if (tar_vel - 1)<=act_vel and act_vel<=tar_vel+1:
                error_sum=0
            flag=1


    error = tar_vel - act_vel
    error_sum += error
    error_diff = error - prev_error
    prev_error = error

    if error > 0 :
        output = kp*error + ki*error_sum + kd*error_diff + kx

    if error < 0 :
        output = kp*error + ki*error_sum + kd*error_diff

    output = int(output)

    if output > 100 :
        output = 100
    if output < -100 :
        output = -100

    pub.publish(output)

def start():
	global pub
	pub = rospy.Publisher('accel', Int16, queue_size=10)
	rospy.Subscriber("joy",Joy, callback_joy)
    	rospy.Subscriber("chatter", Int16, callback_can)
	rospy.init_node('JoyPubli')
	rospy.spin()
if __name__ == '__main__':
	start()
