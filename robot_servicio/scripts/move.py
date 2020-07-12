#!/usr/bin/env python

import math
import rospy
import actionlib
from move_base_msgs.msg import MoveBaseAction, MoveBaseGoal
from geometry_msgs.msg import Pose, Quaternion
from tf.transformations import quaternion_from_euler
from std_msgs.msg import String
import send_goals


class receive_goals():
    def __init__(self):
        self.new_pose = Pose()
        self.received_goals = []
        rospy.Subscriber("/create1/move_base_goals", String, self.register_goal)
        self.listen_positions()


    def register_goal(self, position_goal):
        self.received_goals.append(position_goal.data)


    def listen_positions(self):
        r = rospy.Rate(1) # 1hz
        while not rospy.is_shutdown():
            if self.received_goals:
                self.move_to_goal(self.received_goals.pop())
                send_goals.print_menu()
                
            r.sleep()


    def move_to_goal(self, position_goal):
        param_path = "/table_positions/" + position_goal
        param_data = rospy.get_param(param_path, "None")
        if (param_data == "None"):
            rospy.logerr("[MOVE] Wrong position received")
            return

        rospy.logwarn("[MOVE] Moving to %s", position_goal)

        self.load_position(param_data['x'], param_data['y'], param_data['angle_raw'])

        client = actionlib.SimpleActionClient('move_base', MoveBaseAction)
        client.wait_for_server()
        goal = MoveBaseGoal()
        goal.target_pose.header.frame_id = "map"
        goal.target_pose.header.stamp = rospy.Time.now()
        goal.target_pose.pose.position.x = self.new_pose.position.x
        goal.target_pose.pose.position.y = self.new_pose.position.y
        goal.target_pose.pose.orientation = self.new_pose.orientation

        client.send_goal(goal)
        wait = client.wait_for_result()
        if not wait:
            rospy.logerr("[MOVE] Action server not available!")
            #rospy.signal_shutdown("Action server not available!")
        else:
            if client.get_result():
                rospy.logwarn("[MOVE] Move success")
            else:
                rospy.logerr("[MOVE] Move not done")


    def load_position(self, x, y, angle_raw):
        q = quaternion_from_euler(0, 0, math.pi * angle_raw / 180)
        self.new_pose.position.x = x
        self.new_pose.position.y = y
        self.new_pose.orientation.x = q[0]
        self.new_pose.orientation.y = q[1]
        self.new_pose.orientation.z = q[2]
        self.new_pose.orientation.w = q[3]


if __name__ == '__main__':
    rospy.init_node('move')
    receive_goals()