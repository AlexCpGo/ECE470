#!/usr/bin/env python

'''
We get inspirations of Tower of Hanoi algorithm from the website below.
This is also on the lab manual.
Source: https://www.cut-the-knot.org/recurrence/hanoi.shtml
'''

import copy
import time
import rospy
import actionlib
import numpy as np
from lab2_header import *

# 20Hz
SPIN_RATE = 30
 
# UR3 home location
home = np.radians([-94.30, -91.40, -75.12, -83.49, 91.96, 127.02])
 
# UR3 current position, using home position for initialization
current_position = copy.deepcopy(home)
 
thetas = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
 
digital_in_0 = 0
analog_in_0 = 0
 
suction_on = True
suction_off = False
 
current_io_0 = False
current_position_set = False

############## Your Code Start Here ##############
 
"""
TODO: Definition of position of our tower in Q
"""
Q02 = np.radians([-102.07, -119.49, -85.66, -47.94, 89.93, 127.06])
Q01 = np.radians([-105.23, -122.23, -86.10, -39.89, 90.60, 127.06])
Q00 = np.radians([-104.80, -126.30, -85.49, -37.80, 89.12, 127.06])
Q12 = np.radians([-107.26, -117.26, -72.46, -43.76, 89.98, 127.06])
Q11 = np.radians([-107.45, -121.05, -72.42, -41.03, 89.42, 127.06])
Q10 = np.radians([-109.72, -124.51, -72.36, -34.55, 89.72, 127.06])
Q22 = np.radians([-106.58, -117.71, -59.23, -43.72, 89.05, 127.06])
Q21 = np.radians([-105.04, -121.10, -59.40, -44.50, 89.03, 127.06])
Q20 = np.radians([-107.26, -124.81, -59.45, -37.83, 89.09, 127.06])
Q = [[Q00,Q01,Q02],[Q10,Q11,Q12],[Q20,Q21,Q22]]


############### Your Code End Here ###############
 
 

 
 
############## Your Code Start Here ##############
 
"""
TODO: define a ROS topic callback funtion for getting the state of suction cup
Whenever /ur_hardware_interface/io_states publishes info this callback function is called.
"""
def gripper_input_callback(msg):

	global current_io_0
	current_io_0 = msg.digital_in_states[0].state

############### Your Code End Here ###############
 
 
"""
Whenever ur3/position publishes info, this callback function is called.
"""
def position_callback(msg):
 
	global thetas
	global current_position
	global current_position_set
 
	thetas[0] = msg.position[0]
	thetas[1] = msg.position[1]
	thetas[2] = msg.position[2]
	thetas[3] = msg.position[3]
	thetas[4] = msg.position[4]
	thetas[5] = msg.position[5]

	current_position[0] = thetas[0]
	current_position[1] = thetas[1]
	current_position[2] = thetas[2]
	current_position[3] = thetas[3]
	current_position[4] = thetas[4]
	current_position[5] = thetas[5]

	current_position_set = True


############## Your Code Start Here ##############

def gripper(pub_setio, io_0):

	io = Digital()
	io.pin = 0
	io.state = io_0
	pub_setio.publish(io)
 

############### Your Code End Here ###############
 
def move_arm(pub_setjoint, dest):
	msg = JointTrajectory()
	msg.joint_names = ["elbow_joint", "shoulder_lift_joint", "shoulder_pan_joint","wrist_1_joint", "wrist_2_joint", "wrist_3_joint"]
	point = JointTrajectoryPoint()
	point.positions = dest
	point.time_from_start = rospy.Duration(2)
	msg.points.append(point)
	pub_setjoint.publish(msg)
	time.sleep(2.5)
 
 	
 
 
############## Your Code Start Here ##############
"""
TODO: function to move block from start to end
"""
### Hint: Use the Q array to map out your towers by location and "height".

def move_block(pub_setjoint, pub_setio, start_loc, start_height, end_loc, end_height):
	global Q
	
	start= Q[int(start_loc)-1][start_height]
	end = Q[int(end_loc)-1][end_height]

	move_arm(pub_setjoint, home)
	move_arm(pub_setjoint, start)
	time.sleep(0.5)
	gripper(pub_setio,suction_on)
	move_arm(pub_setjoint, home)
	move_arm(pub_setjoint, end)
	time.sleep(0.5)
	gripper(pub_setio,suction_off)
	time.sleep(1)

############### Your Code End Here ###############
 
 
def main():
 
	global home
	global Q
	global SPIN_RATE

    # Definition of our tower

    # 2D layers (top view)

    # Layer (Above blocks)
    # | Q[0][2][1] Q[1][2][1] Q[2][2][1] |   Above third block
    # | Q[0][1][1] Q[1][1][1] Q[2][1][1] |   Above point of second block
    # | Q[0][0][1] Q[1][0][1] Q[2][0][1] |   Above point of bottom block

    # Layer (Gripping blocks)
    # | Q[0][2][0] Q[1][2][0] Q[2][2][0] |   Contact point of third block
    # | Q[0][1][0] Q[1][1][0] Q[2][1][0] |   Contact point of second block
    # | Q[0][0][0] Q[1][0][0] Q[2][0][0] |   Contact point of bottom block

    # First index - From left to right position A, B, C
    # Second index - From "bottom" to "top" position 1, 2, 3
    # Third index - From gripper contact point to "in the air" point

    # How the arm will move (Suggestions)
    # 1. Go to the "above (start) block" position from its base position
    # 2. Drop to the "contact (start) block" position
    # 3. Rise back to the "above (start) block" position
    # 4. Move to the destination "above (end) block" position
    # 5. Drop to the corresponding "contact (end) block" position
    # 6. Rise back to the "above (end) block" position

	# Initialize ROS node
	rospy.init_node('lab2node')
 
    # Initialize publisher for ur3e_driver_ece470/setjoint with buffer size of 10

	pub_setjoint = rospy.Publisher('ur3e_driver_ece470/setjoint',JointTrajectory,queue_size=10)
	
	############## Your Code Start Here ##############
	# TODO: define a ROS publisher for /ur3e_driver_ece470/setio message 
 
 	pub_setio = rospy.Publisher('/ur3e_driver_ece470/setio',Digital,queue_size=10)
 
	############### Your Code End Here ###############


	# Initialize subscriber to /joint_states and callback fuction
	# each time data is published
	sub_position = rospy.Subscriber('/joint_states', JointState, position_callback)
 
	############## Your Code Start Here ##############
	# TODO: define a ROS subscriber for /ur_hardware_interface/io_states message and corresponding callback function
 
 	sub_setio = rospy.Subscriber('/ur_hardware_interface/io_states', IOStates, gripper_input_callback)
 
	############### Your Code End Here ###############
 
 
	############## Your Code Start Here ##############
	# TODO: modify the code below so that program can get user input
 
	input_done = 0

	while(input_done == 0):
		input_string1 = raw_input("Enter the start position <Either 1 2 3 or 0 to quit> ")
		input_string2 = raw_input("Enter the end position <Either 1 2 3 or 0 to quit> ")
		print("Please Confirm that the following information:")
		print("Your entered start positioon is " + input_string2 + ".\n")
		print("You entered end position" + input_string1 + ".\n")
		if(int(input_string1) == int(input_string2)):
			print("The start point and destination point are same, quitting...")
			sys.exit()	

		elif (int(input_string1) == 0):
			print("Quitting... ")
			sys.exit()
		else:
            #print("Please just enter the character 1 2 3 or 0 to quit \n\n")
			input_done = 1


	############### Your Code End Here ###############
 
	# Check if ROS is ready for operation
	while(rospy.is_shutdown()):
		print("ROS is shutdown!")
 
	rospy.loginfo("Sending Goals ...")
 
	loop_rate = rospy.Rate(SPIN_RATE)
 
	############## Your Code Start Here ##############
	# TODO: modify the code so that UR3 can move tower accordingly from user input
 

	start = input_string1
	end = input_string2
	median = 0
	if (start == '1' and end == '2'):
		median = '3'
	elif (start == '1' and end == '3'):
		median= '2'
	elif (start == '2' and end == '1'):
		median = '3'
	elif (start == '2' and end == '3'):
		median = '1'
	elif (start == '3' and end== '1'):
		median = '2'
	elif (start== '3' and end == '2'):
		median = '1'
	
	move_arm(pub_setjoint, home)
	move_block(pub_setjoint, pub_setio, start, 2, end,   0)
	move_block(pub_setjoint, pub_setio, start, 1, median,   0)
	move_block(pub_setjoint, pub_setio, end, 0, median,   1)
	move_block(pub_setjoint, pub_setio, start, 0, end,   0)
	move_block(pub_setjoint, pub_setio, median , 1, start,   0)
	move_block(pub_setjoint, pub_setio, median, 0, end   1)
	move_block(pub_setjoint, pub_setio, start 0, end,   2)


	############### Your Code End Here ###############
 
 
 
if __name__ == '__main__':
	
	try:
		main()
    # When Ctrl+C is executed, it catches the exception
	except rospy.ROSInterruptException:
		pass
 
 
	
 
