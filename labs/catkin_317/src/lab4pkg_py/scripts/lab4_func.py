#!/usr/bin/env python
import numpy as np
from scipy.linalg import expm
from lab4_header import *
import math
from math import asin as asin
from math import acos as acos
from math import atan2 as atan2
from math import atan as atan
from math import sin as sin
from math import cos as cos
from math import pi as PI
"""
Use 'expm' for matrix exponential.
Angles are in radian, distance are in meters.
Add any helper functions as you need.
"""
def Get_MS():
	# =================== Your code starts here ====================#
	# Fill in the correct values for a1~6 and q1~6, as well as the M matrix
	M = np.eye(4)
	S = np.zeros((6,6))


	
	# ==============================================================#
	return M, S


"""
Function that calculates encoder numbers for each motor
"""
def lab_fk(theta1, theta2, theta3, theta4, theta5, theta6):

	# Initialize the return_value 
	return_value = [None, None, None, None, None, None]

	print("Foward kinematics calculated:\n")

	# =================== Your code starts here ====================#
	theta = np.array([theta1,theta2,theta3,theta4,theta5,theta6])
	T = np.eye(4)

	M, S = Get_MS()








	# ==============================================================#
	
	print(str(T) + "\n")

	return_value[0] = theta3
	return_value[1] = theta2
	return_value[2] = theta1 + (0.5*PI)
	return_value[3] = theta4 - (0.5*PI)
	return_value[4] = theta5
	return_value[5] = theta6

	return return_value


"""
Function that calculates an elbow up Inverse Kinematic solution for the UR3
"""
def lab_invk(xWgrip, yWgrip, zWgrip, yaw_WgripDegree):

    # theta1 to theta6
	thetas = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0]

	l01 = 0.152
	l02 = 0.120
	l03 = 0.244
	l04 = 0.093
	l05 = 0.213
	l06 = 0.104
	l07 = 0.085
	l08 = 0.092
	l09 = 0
	l10 = 0.0   # thickness of aluminum plate is around 0.01

	xgrip = -(yWgrip)
	ygrip = xWgrip
	zgrip = zWgrip-0.015

	xcen = xgrip
	ycen = ygrip
	zcen = zgrip

	# theta1
	thetas[0] = math.atan2(ygrip,xgrip)-asin((l02-l04+l06)/(xcen**2+ycen**2)**0.5)       # Default value Need to Change

	# theta6
	thetas[5] = 0     # Default value Need to Change
 
	x3end = (((xcen**2+ycen**2)-(l02-l04+l06)**2)**0.5-l07)*cos(thetas[0])
	y3end = (((xcen**2+ycen**2)-(l02-l04+l06)**2)**0.5-l07)*sin(thetas[0])
	z3end = zcen + l08
	lend=(x3end**2+y3end**2+(z3end-l01)**2)**0.5
	thetas[2]= PI-acos((lend**2-l03**2-l05**2)/(-2*l03*l05))
	thetas[1]= -acos((-lend**2-l03**2+l05**2)/(-2*l03*lend))- atan((z3end-l01)/(x3end**2+y3end**2)**0.5)    # Default value Need to Change
	     # Default value Need to Change
	thetas[3]= -thetas[1] - thetas[2] # Default value Need to Change
	thetas[4]=-PI/2      

	print("theta1 to theta6: " + str(thetas) + "\n")

	
	return lab_fk(float(thetas[0]), float(thetas[1]), float(thetas[2]), \
		          float(thetas[3]), float(thetas[4]), float(thetas[5]) )
