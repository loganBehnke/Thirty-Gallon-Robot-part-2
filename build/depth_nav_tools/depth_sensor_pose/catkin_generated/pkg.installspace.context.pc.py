# generated from catkin/cmake/template/pkg.context.pc.in
CATKIN_PACKAGE_PREFIX = ""
PROJECT_PKG_CONFIG_INCLUDE_DIRS = "${prefix}/include".split(';') if "${prefix}/include" != "" else []
PROJECT_CATKIN_DEPENDS = "roscpp;dynamic_reconfigure;image_geometry;image_transport;nodelet;sensor_msgs;libpcl-all".replace(';', ' ')
PKG_CONFIG_LIBRARIES_WITH_PREFIX = "-lDepthSensorPose;-lDepthSensorPoseNode;-lDepthSensorPoseNodelet".split(';') if "-lDepthSensorPose;-lDepthSensorPoseNode;-lDepthSensorPoseNodelet" != "" else []
PROJECT_NAME = "depth_sensor_pose"
PROJECT_SPACE_DIR = "/home/student/RAT/Thirty-Gallon-Robot-part-2/install"
PROJECT_VERSION = "1.0.0"
