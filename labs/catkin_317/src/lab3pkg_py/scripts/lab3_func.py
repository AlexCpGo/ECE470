#!/usr/bin/env python
import numpy as np
from scipy.linalg import expm
from lab3_header import *

"""
Use 'expm' for matrix exponential.
Angles are in radian, distance are in meters.
You may write some helper functions as you need.
"""

def Get_MS():
	# =================== Your code starts here ====================#
	# Fill in the correct values for S1~6, as well as the M matrix
	M = np.eye(4)
	S = np.zeros((6,6))
	w1=np.array([0,0,1])
	q1=np.array([0,0,0])+np.array([100,100,0])
	w2=np.array([1,0,0])
	q2=q1+np.array([120,0,152])
	w3=np.array([1,0,0])
	q3=q2+np.array([0,-244,0])	
	w4=np.array([1,0,0])
	q4=q3+np.array([-93,-213,0])	
	w5=np.array([0,-1,0])
	q5=q4+np.array([104,0,0])
	w6=np.array([1,0,0])
	q6=q5+np.array([92,-85,0])
	
	v1=-np.cross(w1,q1)
	v2=-np.cross(w2,q2)
	v3=-np.cross(w3,q3)
	v4=-np.cross(w4,q4)
	v5=-np.cross(w5,q5)
	v6=-np.cross(w6,q6)
	"""
	s1=np.array(([[0,-w1[2],w1[1],v1[0]],
		      [w1[2],0,-w1[0],v1[1]],
		      [-w1[1],w1[0],0,v1[2]],
		      [0,0,0,0]])
	"""
	S[0,:]=np.array([w1[0],w1[1],w1[2],v1[0],v1[1],v1[2]])
	S[1,:]=np.array([w2[0],w2[1],w2[2],v2[0],v2[1],v2[2]])
	S[2,:]=np.array([w3[0],w3[1],w3[2],v3[0],v3[1],v3[2]])
	S[3,:]=np.array([w4[0],w4[1],w4[2],v4[0],v4[1],v4[2]])
	S[4,:]=np.array([w5[0],w5[1],w5[2],v5[0],v5[1],v5[2]])
	S[5,:]=np.array([w6[0],w6[1],w6[2],v6[0],v6[1],v6[2]])
	M=np.array([[0,1,0,q6[0]],
		     [-1,0,0,q6[1]],
		     [0,0,1,q6[2]],
		     [0,0,0,1]])
	# ==============================================================#
	return M, S


"""
Function that calculates encoder numbers for each motor
"""
def lab_fk(theta1, theta2, theta3, theta4, theta5, theta6):

	# Initialize the return_value 
	return_value = [None, None, None, None, None, None]

	# =========== Implement joint angle to encoder expressions here ===========
	print("Foward kinematics calculated:\n")

	# =================== Your code starts here ====================#
	theta = np.array([theta1,theta2,theta3,theta4,theta5,theta6])
	T = np.eye(4)

	M, S = Get_MS()

	s = np.zeros((6,4,4))

	for i in range(6):
		s[i,:,:] = np.array([[0,-S[i,2],S[i,1],S[i,3]],
		      		      [S[i,2],0,-S[i,0],S[i,4]],
		      		      [-S[i,1],S[i,0],0,S[i,5]],
		      		      [0,0,0,0]])


	for i in range(6):
		T = np.dot(T, expm(np.dot(s[i], theta[i])))

	T = np.dot(T,M)



	# ==============================================================#
	
	print(str(T) + "\n")

	return_value[0] = theta3
	return_value[1] = theta2
	return_value[2] = theta1 + (0.5*PI)
	return_value[3] = theta4 - (0.5*PI)
	return_value[4] = theta5
	return_value[5] = theta6

	return return_value


