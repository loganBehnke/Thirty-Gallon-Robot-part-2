# generated from catkin/cmake/template/pkg.context.pc.in
CATKIN_PACKAGE_PREFIX = ""
PROJECT_PKG_CONFIG_INCLUDE_DIRS = "${prefix}/include".split(';') if "${prefix}/include" != "" else []
PROJECT_CATKIN_DEPENDS = "roscpp;dynamic_reconfigure;image_geometry;image_transport;nodelet;sensor_msgs".replace(';', ' ')
PKG_CONFIG_LIBRARIES_WITH_PREFIX = "-lLaserScanKinect;-lLaserScanKinectNode;-lLaserScanKinectNodelet".split(';') if "-lLaserScanKinect;-lLaserScanKinectNode;-lLaserScanKinectNodelet" != "" else []
PROJECT_NAME = "laserscan_kinect"
PROJECT_SPACE_DIR = "/home/student/RAT/Thirty-Gallon-Robot-part-2/install"
PROJECT_VERSION = "1.0.1"
