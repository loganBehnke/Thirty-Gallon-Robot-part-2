#!/usr/bin/env python
import rospy
import socket
import tf
from geometry_msgs.msg import Pose

if __name__ == '__main__':
    rospy.init_node('tf_listener')
    listener = tf.TransformListener()

    rate = rospy.Rate(10.0)
    while not rospy.is_shutdown():
        try:
            (trans, rot) = listener.lookupTransform('/base_link', '/map', rospy.Time(0))
        except (tf.LookupException, tf.ConnectivityException, tf.ExtrapolationException):
            continue

        try:
            #s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            #s.connect(('rat-tracker.herokuapp.com', 1234))
            msgs = '{}, {}'.format(round(trans[0],4), round(trans[1], 4))
            print(msgs)
            rospy.loginfo(msgs)
            #s.send(msgs)
            #s.shutdown(1)
            #s.close()
        except OSError as error:
            print("error: {0}".format(error))