# -*- coding: utf-8 -*-
from __future__ import print_function
import argparse
import os
import stat
import sys

# find the import for catkin's python package - either from source space or from an installed underlay
if os.path.exists(os.path.join('/opt/ros/kinetic/share/catkin/cmake', 'catkinConfig.cmake.in')):
    sys.path.insert(0, os.path.join('/opt/ros/kinetic/share/catkin/cmake', '..', 'python'))
try:
    from catkin.environment_cache import generate_environment_script
except ImportError:
    # search for catkin package in all workspaces and prepend to path
    for workspace in "/home/ur3/catkin_ws/devel_isolated/ur_robot_driver;/home/ur3/catkin_ws/devel_isolated/ur_msgs;/home/ur3/catkin_ws/devel_isolated/ur_kinematics;/home/ur3/catkin_ws/devel_isolated/ur_gazebo;/home/ur3/catkin_ws/devel_isolated/ur_e_gazebo;/home/ur3/catkin_ws/devel_isolated/ur_e_description;/home/ur3/catkin_ws/devel_isolated/ur_driver;/home/ur3/catkin_ws/devel_isolated/ur5_moveit_config;/home/ur3/catkin_ws/devel_isolated/ur5_e_moveit_config;/home/ur3/catkin_ws/devel_isolated/ur3_moveit_config;/home/ur3/catkin_ws/devel_isolated/ur3_e_moveit_config;/home/ur3/catkin_ws/devel_isolated/ur10_moveit_config;/home/ur3/catkin_ws/devel_isolated/ur10_e_moveit_config;/home/ur3/catkin_ws/devel_isolated/ur_description;/home/ur3/catkin_ws/devel_isolated/ur_dashboard_msgs;/home/ur3/catkin_ws/devel_isolated/ur_controllers;/home/ur3/catkin_ws/devel_isolated/ur_calibration;/home/ur3/catkin_ws/devel_isolated/ur_client_library;/home/ur3/catkin_ws/devel_isolated/ur_bringup;/home/ur3/catkin_ws/devel_isolated/universal_robots;/home/ur3/catkin_ws/devel_isolated/universal_robot;/home/ur3/catkin_ws/devel_isolated/controller_stopper;/opt/ros/kinetic".split(';'):
        python_path = os.path.join(workspace, 'lib/python2.7/dist-packages')
        if os.path.isdir(os.path.join(python_path, 'catkin')):
            sys.path.insert(0, python_path)
            break
    from catkin.environment_cache import generate_environment_script

code = generate_environment_script('/home/ur3/catkin_317/devel/env.sh')

output_filename = '/home/ur3/catkin_317/build/catkin_generated/setup_cached.sh'
with open(output_filename, 'w') as f:
    #print('Generate script for cached setup "%s"' % output_filename)
    f.write('\n'.join(code))

mode = os.stat(output_filename).st_mode
os.chmod(output_filename, mode | stat.S_IXUSR)
