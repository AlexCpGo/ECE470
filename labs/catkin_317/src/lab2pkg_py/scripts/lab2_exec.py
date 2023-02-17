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
SPIN_RATE = 20 
 
# UR3 home location
home = np.radians([-87.42, -103.45, -72.77, -79.02, 89.95, 129.93])
 
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
Q = np.zeros((3,3,6))
Q[0][0]=np.radians([-106.76,-125.18,-80.95,-37.99,89.96,154.35])
Q[1][0]=np.radians([-109.15,-123.77,-67.98,-36.42,89.96,167.33])
Q[2][0]=np.radians([-105.17,-125.67,-55.81,-38.51,89.83,179.50])
Q[2][1]=np.radians([-104.38,-122.46,-55.82,-42.47,89.85,179.49])
Q[1][1]=np.radians([-108.32,-120.38,-68.00,-40.60,89.98,167.31])
Q[0][1]=np.radians([-105.87,-121.67,-81.39,-41.78,90.13,153.92])
Q[0][2]=np.radians([-104.33,-117.85,-81.39,-47.14,90.14,153.92])
Q[1][2]=np.radians([-106.75,-116.41,-68.00,-46.13,89.99,167.31])
Q[2][2]=np.radians([-102.83,-118.69,-55.82,-47.78,89.85,179.48])


 
############### Your Code End Here ###############
 
 

 
 
############## Your Code Start Here ##############
 
"""
TODO: define a ROS topic callback funtion for getting the state of suction cup
Whenever /ur_hardware_interface/io_states publishes info this callback function is called.
"""
def gripper_input_callback(msg):
	digital_in_0 = msg.digital_in_states[0].state


 
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
	msg = Digital()
	msg.pin = 0
	msg.state = io_0
	pub_setio.publish(msg)
	time.sleep(2.5)

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
 	move_arm(pub_setjoint,Q[start_loc][start_height])
	gripper(pub_setio,suction_on)
	move_arm(pub_setjoint,home)
	move_arm(pub_setjoint,Q[end_loc][end_height])
	gripper(pub_setio,suction_off)
	move_arm(pub_setjoint,home)
 
 
 
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
 
 	pub_setio= rospy.Publisher('ur3e_driver_ece470/setio',Digital,queue_size=10)

 
	############### Your Code End Here ###############


	# Initialize subscriber to /joint_states and callback fuction
	# each time data is published
	sub_position = rospy.Subscriber('/joint_states', JointState, position_callback)
 
	############## Your Code Start Here ##############
	# TODO: define a ROS subscriber for /ur_hardware_interface/io_states message and corresponding callback function
 
 	sub_gripper = rospy.Subscriber('/ur_hardware_interface/io_states', IOStates, gripper_input_callback)
 
	############### Your Code End Here ###############
 
 
	############## Your Code Start Here ##############
	# TODO: modify the code below so that program can get user input
 
	input_done = 0
	start_point = 0

	while(not input_done):
        	input_string = raw_input("Enter start point <Either 1 2 3 or 0 to quit> ")
		print("You entered " + input_string + "\n")

		if(int(input_string) == 1):
			input_done = 1
			start_point = 1
		elif (int(input_string) == 2):
			input_done = 1
			start_point = 2
        	elif (int(input_string) == 3):
			input_done = 1
			start_point = 3
		elif (int(input_string) == 0):
			print("Quitting... ")
			sys.exit()
		else:
			print("Please just enter the character 1 2 3 or 0 to quit \n\n")
	input_done = 0
	end_point = 0

	while(not input_done):
        	input_string = raw_input("Enter end point <Either 1 2 3 or 0 to quit> ")
		print("You entered " + input_string + "\n")

		if(int(input_string) == 1):
			input_done = 1
			end_point = 1
		elif (int(input_string) == 2):
			input_done = 1
			end_point = 2
        	elif (int(input_string) == 3):
			input_done = 1
			end_point = 3
		elif (int(input_string) == 0):
			print("Quitting... ")
			sys.exit()
		else:
			print("Please just enter the character 1 2 3 or 0 to quit \n\n")



			

	############### Your Code End Here ###############
 
	# Check if ROS is ready for operation
	while(rospy.is_shutdown()):
		print("ROS is shutdown!")
 
	rospy.loginfo("Sending Goals ...")
 
	loop_rate = rospy.Rate(SPIN_RATE)
 
	############## Your Code Start Here ##############
	# TODO: modify the code so that UR3 can move tower accordingly from user input
 
	move_arm(pub_setjoint, home)
	a=start_point-1
	b=end_point-1
	c=3-a-b
	move_block(pub_setjoint, pub_setio, a, 2, b,   0)
	move_block(pub_setjoint, pub_setio, a, 1, c,   0)
	move_block(pub_setjoint, pub_setio, b, 0, c,   1)
	move_block(pub_setjoint, pub_setio, a, 0, b,   0)
	move_block(pub_setjoint, pub_setio, c, 1, a,   0)
	move_block(pub_setjoint, pub_setio, c, 0, b,   1)
	move_block(pub_setjoint, pub_setio, a, 0, b,   2)




	
 
 
	############### Your Code End Here ###############
 
 
if __name__ == '__main__':
	
	try:
		main()
    # When Ctrl+C is executed, it catches the exception
	except rospy.ROSInterruptException:
		pass
 
 
	
 
