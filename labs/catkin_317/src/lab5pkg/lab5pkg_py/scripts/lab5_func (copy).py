#!/usr/bin/env python
import numpy as np
from scipy.linalg import expm
from lab5_header import *
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
	
	S = np.zeros((6,6))
	M = np.array([[1,0,0,293],[0,1,0,-542],[0,0,1,152],[0,0,0,1]])
	
	w1 = np.array([0,0,1])
	q1 = np.array([0,0,152])
	v1 = -np.cross(w1,q1)

	w2 = np.array([1,0,0])
	q2 = np.array([120,0,152])
	v2 = -np.cross(w2,q2)

	w3 = np.array([1,0,0])
	q3 = q2-np.array([0,244,0])
	v3 = -np.cross(w3,q3)
	
	w4 = np.array([1,0,0])
	q4 = q3-np.array([93,213,0])
	v4 = -np.cross(w4,q4)
	
	w5 = np.array([0,-1,0])
	q5 = q4+np.array([104,0,0])
	v5 = -np.cross(w5,q5)

	w6 = np.array([1,0,0])
	q6 = q5+np.array([92,0,0])
	v6 = -np.cross(w6,q6)
	

	for j in range(3):
		S[j][0]=w1[j]
		S[j+3][0]=v1[j]
	for j in range(3):
		S[j][1]=w2[j]
		S[j+3][1]=v2[j]
	for j in range(3):
		S[j][2]=w3[j]
		S[j+3][2]=v3[j]
	for j in range(3):
		S[j][3]=w4[j]
		S[j+3][3]=v4[j]
	for j in range(3):
		S[j][4]=w5[j]
		S[j+3][4]=v5[j]
	for j in range(3):
		S[j][5]=w6[j]
		S[j+3][5]=v6[j]



	
	# ==============================================================#
	return M, S


"""
Function that calculates encoder numbers for each motor
"""
def lab_fk(theta1, theta2, theta3, theta4, theta5, theta6):

	# Initialize the return_value 
	return_value = [None, None, None, None, None, None]

	#print("Foward kinematics calculated:\n")

	# =================== Your code starts here ====================#
	theta = np.array([theta1,theta2,theta3,theta4,theta5,theta6])
	

	M, S = Get_MS()

	S1 = np.array([[0, -S[2,0], S[1,0], S[3,0]],[S[2,0], 0, -S[0,0], S[4,0]],[-S[1,0], S[0,0], 0, S[5,0]], [0 ,0 ,0 ,0]])
	S2 = np.array([[0, -S[2,1], S[1,1], S[3,1]],[S[2,1], 0, -S[0,1], S[4,1]],[-S[1,1], S[0,1], 0, S[5,1]], [0 ,0 ,0 ,0]])
	S3 = np.array([[0, -S[2,2], S[1,2], S[3,2]],[S[2,2], 0, -S[0,2], S[4,2]],[-S[1,2], S[0,2], 0, S[5,2]], [0 ,0 ,0 ,0]])
	S4 = np.array([[0, -S[2,3], S[1,3], S[3,3]],[S[2,3], 0, -S[0,3], S[4,3]],[-S[1,3], S[0,3], 0, S[5,3]], [0 ,0 ,0 ,0]])
	S5 = np.array([[0, -S[2,4], S[1,4], S[3,4]],[S[2,4], 0, -S[0,4], S[4,4]],[-S[1,4], S[0,4], 0, S[5,4]], [0 ,0 ,0 ,0]])
	S6 = np.array([[0, -S[2,5], S[1,5], S[3,5]],[S[2,5], 0, -S[0,5], S[4,5]],[-S[1,5], S[0,5], 0, S[5,5]], [0 ,0 ,0 ,0]])
	T1 = expm(np.dot(S1,theta1))
	T2 = np.dot(T1,expm(np.dot(S2,theta2)))
	T3 = np.dot(T2,expm(np.dot(S3,theta3)))
	T4 = np.dot(T3,expm(np.dot(S4,theta4)))
	T5 = np.dot(T4,expm(np.dot(S5,theta5)))
	T6 = np.dot(T5,expm(np.dot(S6,theta6)))
	T = np.dot(T6,M)

	




	# ==============================================================#
	
	#print(str(T) + "\n")

	return_value[0] = theta3
	return_value[1] = theta2
	return_value[2] = theta1 + (0.5*PI)
	return_value[3] = theta4 - (0.5*PI)
	return_value[4] = theta5
	return_value[5] = theta6

	return return_value

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

	xgrip = -yWgrip
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
"""
Function that calculates an elbow up Inverse Kinematic solution for the UR3
"""



