#include "ros/ros.h"
#include "ur_msgs/SetIO.h"
#include "ur_msgs/Digital.h" 
#include <actionlib/client/simple_action_client.h>
#include "control_msgs/FollowJointTrajectoryAction.h"
#include "control_msgs/FollowJointTrajectoryGoal.h"
#include "control_msgs/FollowJointTrajectoryResult.h"
#include "control_msgs/FollowJointTrajectoryFeedback.h"
#include "trajectory_msgs/JointTrajectory.h"
#include "trajectory_msgs/JointTrajectoryPoint.h"

typedef actionlib::SimpleActionClient<control_msgs::FollowJointTrajectoryAction> Client;

void SetIOCallback(const ur_msgs::Digital& msg)
{
	uint8_t Pin = msg.pin;
	bool State = msg.state;
	ros::NodeHandle nh;
	ros::ServiceClient setio_ser_client = nh.serviceClient<ur_msgs::SetIO>("ur_hardware_interface/set_io");
	ur_msgs::SetIO srv;
	srv.request.fun = 1;
	srv.request.pin = Pin;
	if(State)
		srv.request.state = 1;
	else
		srv.request.state = 0;
	if(setio_ser_client.call(srv))
	{
		ROS_INFO_STREAM("success to set io!");
	}
	else{
		ROS_INFO_STREAM("fail to set io!");
	}
	return;
}

void done(const actionlib::SimpleClientGoalState& state,const control_msgs::FollowJointTrajectoryResultConstPtr& result){
	ROS_INFO_STREAM(state.toString().c_str());
}
void active(){}
void feedback(const control_msgs::FollowJointTrajectoryFeedbackConstPtr& feedback){}

void SetJointCallback(const trajectory_msgs::JointTrajectory& msg)
{
	Client setjoint_act_client("scaled_pos_joint_traj_controller/follow_joint_trajectory",true);

	ROS_INFO_STREAM("Waiting for action server to start.");
	setjoint_act_client.waitForServer();
	ROS_INFO_STREAM("Action server started.");

	control_msgs::FollowJointTrajectoryGoal goal;
	goal.trajectory = msg;
	setjoint_act_client.sendGoal(goal,&done,&active,&feedback);

	// goal.trajectory.joint_names.push_back("elbow_joint");
	// goal.trajectory.joint_names.push_back("shoulder_lift_joint");
	// goal.trajectory.joint_names.push_back("shoulder_pan_joint");
	// goal.trajectory.joint_names.push_back("wrist_1_joint");
	// goal.trajectory.joint_names.push_back("wrist_2_joint");
	// goal.trajectory.joint_names.push_back("wrist_3_joint");	
	
    // trajectory_msgs::JointTrajectoryPoint point;
	// point.positions.push_back(-1.523);
	// point.positions.push_back(-1.991);
	// point.positions.push_back(-1.280);
	// point.positions.push_back(-1.190);
	// point.positions.push_back(1.510);
	// point.positions.push_back(0.414);
	// point.time_from_start = ros::Duration(5);
	// goal.trajectory.points.push_back(point);
}
/**
 * This tutorial demonstrates simple sending of messages over the ROS system.
 */
int main(int argc, char *argv[])
{
	/**
	 * The ros::init() function needs to see argc and argv so that it can perform
	 * any ROS arguments and name remapping that were provided at the command line.
	 * For programmatic remappings you can use a different version of init() which takes
	 * remappings directly, but for most command-line programs, passing argc and argv is
	 * the easiest way to do it.  The third argument to init() is the name of the node.
	 *
	 * You must call one of the versions of ros::init() before using any other
	 * part of the ROS system.
	 */
	ros::init(argc, argv, "ur3e_driver_ece470");

	/**
	 * NodeHandle is the main access point to communications with the ROS system.
	 * The first NodeHandle constructed will fully initialize this node, and the last
	 * NodeHandle destructed will close down the node.
	 */
	ros::NodeHandle nh;

	ros::Subscriber setio_sub = nh.subscribe("ur3e_driver_ece470/setio", 10, SetIOCallback);

	ros::Subscriber setjoint_sub = nh.subscribe("ur3e_driver_ece470/setjoint", 10, SetJointCallback);	

	ros::Rate loop_rate(10);

	while (ros::ok())
	{
		ros::spinOnce();

		loop_rate.sleep();
	}

	return 0;
}