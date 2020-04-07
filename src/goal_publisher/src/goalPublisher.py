#!/usr/bin/env python
import rospy
import actionlib
import socket
from move_base_msgs.msg import MoveBaseAction, MoveBaseGoal
from geometry_msgs.msg import Pose

if __name__ == "__main__":
    try:
        rospy.init_node('movebase_client_py')
        #client = actionlib.SimpleActionClient('move_base', MoveBaseAction)
        #client.wait_for_server()
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind(('localhost', 55555))
        s.listen(1)
        print("waiting for connection")
        while not rospy.is_shutdown():
            conn, addr = s.accept()
            results = conn.recv(1024)
            #print("what x, y location do you want RAT to go to?\n")
            #results = raw_input()
            listOfValues = results.split(", ")
            print(listOfValues)
            #goal = MoveBaseGoal()
            #goal.target_pose.header.frame_id = 'base_link'
            #goal.target_pose.header.stamp = rospy.Time.now()
            #goal.target_pose.pose.position.x = int(listOfValues[0])
            #goal.target_pose.pose.position.y = int(listOfValues[1])
            conn.close()
            #client.send_goal(goal)
    except:
        print("there was an error")
