#!/usr/bin/env python
import rospy
import tf
import numpy as np
from std_msgs.msg import Int32
from nav_msgs.msg import Odometry
from geometry_msgs.msg import Point, Quaternion, TransformStamped
from encoder import Encoder

from __init__ import ROSnode

class Odometer(ROSnode):

    def __init__(self):
        self.encoders = [
            Encoder(7, 12, 16, backward=True),
            Encoder(15, 11, 13),
        ]

        self.messageEncs = [
            Int32(),
            Int32(),
        ]

        self.publisherEncs = [
            rospy.Publisher('/encl', Int32, queue_size=24),
            rospy.Publisher('/encr', Int32, queue_size=24)
        ]

        self.sampLOld = self.encoders[0].pos
        self.sampROld = self.encoders[1].pos
        self.theta = 0.0
        self.x = 0.0
        self.y = 0.0
        self.t = self.initTime = rospy.Time.now().to_sec()

        self.frame_id = '/odom'
        self.odom_pub = rospy.Publisher('/odom', Odometry, queue_size=128)
        self.tf_broadcaster = tf.TransformBroadcaster()
        self.child_frame_id = '/base_link'

    CLICKS_PER_M = 64 /(2 * np.pi * 0.3302)

    @property
    def RIGHT_CLICKS_PER_M(self):
        return float(rospy.get_param("~RIGHT_CLICKS_PER_M", self.CLICKS_PER_M))

    @property
    def LEFT_CLICKS_PER_M(self):
        return float(rospy.get_param("~LEFT_CLICKS_PER_M", self.CLICKS_PER_M))

    @property
    def WHEEL_BASE_M(self):
        return float(rospy.get_param("~WHEEL_BASE_M", 0.3177))

    def publish_odom(self, xyz, thxyz, vxyz, vthxyz):
        # initialize Odometry message object.
        msg = Odometry()
        msg.header.stamp = rospy.Time.now()
        msg.header.frame_id = self.frame_id # i.e. '/odom'

        # fill the mesage with data
        msg.pose.pose.position = Point(*xyz)
        quat = tf.transformations.quaternion_from_euler(*thxyz)
        msg.pose.pose.orientation = Quaternion(*quat)

        for i in range(3):
            setattr(msg.twist.twist.linear, 'xyz'[i], vxyz[i])
            setattr(msg.twist.twist.angular, 'xyz'[i], vthxyz[i])

        self.tf_broadcaster.sendTransform(
            xyz,
            quat,
            msg.header.stamp,
            self.child_frame_id,
            self.frame_id,
        )

        P = np.mat(np.diag([0.0]*3)) # Covariance
        p_cov = np.array([0.0]*36).reshape(6,6)
        p_cov[0:2,0:2] = P[0:2,0:2]
        # orientation covariance for yaw
        # x and yaw
        p_cov[5,0] = p_cov[0,5] = P[2,0]
        # y and yaw 
        p_cov[5,1] = p_cov[1,5] = P[2,1]
        # yaw and yaw
        p_cov[5,5] = P[2,2]

        msg.pose.covariance= tuple(p_cov.ravel().tolist())

        self.odom_pub.publish(msg)

    def update(self):

        from math import cos, sin

        # Sample the left and right encoder counts as close together
        # in time as possible.
        sampL, sampR = [enc.pos for enc in self.encoders]
        oldt = self.t
        self.t = rospy.Time.now().to_sec()
        dt = self.t - oldt

        # Detrmine how many ticks have passed since our last sampling.
        dTicksL = sampL - self.sampLOld
        dTicksR = sampR - self.sampROld
        self.sampLOld = sampL
        self.sampROld = sampR

        # convert longs to floats and ticks to meters.
        deltaSlMeters = float(dTicksL) / self.LEFT_CLICKS_PER_M
        deltaSrMeters = float(dTicksR) / self.RIGHT_CLICKS_PER_M

        # Calculate central distance we have traveled since last sample
        deltaSMeters = (deltaSrMeters + deltaSlMeters) / 2.0

        # Accumulate total rotaion around our center (rads)
        # Subtracting L from R gives us a right-handed coordinate system?
        deltaTheta = (deltaSlMeters - deltaSrMeters) / self.WHEEL_BASE_M
        self.theta += deltaTheta

        # Accumulate our transition from the odometry frame (meters)
        deltaX = deltaSMeters * cos(self.theta + deltaTheta / 2.)
        deltaY = deltaSMeters * sin(self.theta + deltaTheta / 2.)
        self.x += deltaX
        self.y += deltaY

        translationRates = (
            deltaX / dt,
            deltaY / dt,
            0.0,
        )

        rotationRates = (
            0.0,
            0.0,
            deltaTheta / dt,
        )

        self.publish_odom(
            (self.x, self.y, 0),
            (0, 0, self.theta),
            translationRates,
            rotationRates)

    def spinOnce(self):
        for enc, pub, msg in zip(self.encoders, self.publisherEncs, self.messageEncs):
            msg.data = enc.pos
            pub.publish(msg)
        self.update()

    def main(self):
        r = rospy.Rate(rospy.get_param("~odometryRate", 10))
        while not rospy.is_shutdown():
            self.spinOnce()
            r.sleep()