# generated from catkin/cmake/template/pkg.context.pc.in
CATKIN_PACKAGE_PREFIX = ""
PROJECT_PKG_CONFIG_INCLUDE_DIRS = "/home/robot-workstation/mapping/devel/include;/home/robot-workstation/mapping/src/depth_nav_tools/cliff_detector/include".split(';') if "/home/robot-workstation/mapping/devel/include;/home/robot-workstation/mapping/src/depth_nav_tools/cliff_detector/include" != "" else []
PROJECT_CATKIN_DEPENDS = "roscpp;dynamic_reconfigure;image_geometry;image_transport;nodelet;sensor_msgs;depth_nav_msgs".replace(';', ' ')
PKG_CONFIG_LIBRARIES_WITH_PREFIX = "-lCliffDetector;-lCliffDetectorNode;-lCliffDetectorNodelet".split(';') if "-lCliffDetector;-lCliffDetectorNode;-lCliffDetectorNodelet" != "" else []
PROJECT_NAME = "cliff_detector"
PROJECT_SPACE_DIR = "/home/robot-workstation/mapping/devel"
PROJECT_VERSION = "1.0.1"
