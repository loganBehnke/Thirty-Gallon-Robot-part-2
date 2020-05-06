#!/usr/bin/env python
import rospy
import os
import actionlib
import socket
import json
from move_base_msgs.msg import MoveBaseAction, MoveBaseGoal
from geometry_msgs.msg import Pose, Point, Quaternion

rooms1st = {"101":(1,1), "elevator":(0,0), "102":(2,2), "103":(3,3)}
rooms2nd = {"201":(35.3, -12.9), "elevator":(-15.5,-16.5), "202":(2,2), "203":(3,3)}
rooms3rd = {"301":(1,1), "elevator":(0,0), "302":(2,2), "303":(3,3)}
if __name__ == "__main__":
    try:
        rospy.init_node('movebase_client_py')
        currentFloor = rospy.get_param("~currentFloor", 2)
        client = actionlib.SimpleActionClient('move_base', MoveBaseAction)
        client.wait_for_server()
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(None)
        s.bind(('localhost', 55555))
        s.listen(1)
        print("waiting for connection")
        while not rospy.is_shutdown():
            conn, addr = s.accept()
            results = conn.recv(1024)
            listOfValues = results.split(", ")
            newFloor = int(listOfValues[0])
            newdestination = listOfValues[1]
            print(listOfValues)
            print(newFloor)
            print(newdestination)
            if(newFloor == currentFloor):
                print("we already on this floor")
                # navigate to room
                if(newFloor == 1):
                    coords = rooms1st[newdestination]
                elif(newFloor == 2):
                    coords = rooms2nd[newdestination]
                elif(newFloor == 3):
                    coords = rooms3rd[newdestination]
                
                goal = MoveBaseGoal()
                goal.target_pose.header.frame_id = 'base_link'
                goal.target_pose.header.stamp = rospy.Time.now()
                goal.target_pose.pose = Pose(Point(coords[0], coords[1], 0.00), Quaternion(0.0,0.0,0.0,1.0))
                print("goal set for moving on this floor")
            else:
                if(currentFloor == 1):
                    coords = rooms1st["elevator"]
                elif(currentFloor == 2):
                    coords = rooms2nd["elevator"]
                elif(currentFloor == 3):
                    coords = rooms3rd["elevator"]
                
                goal = MoveBaseGoal()
                goal.target_pose.header.frame_id = 'base_link'
                goal.target_pose.header.stamp = rospy.Time.now()
                goal.target_pose.pose.position.x = coords[0]
                goal.target_pose.pose.position.y = coords[1]
                goal.target_pose.pose.orientation.w = 1
            
            conn.close()
            client.send_goal(goal)
    except OSError as err:
        print(err)
        print("there was an error")
