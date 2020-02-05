#include "ros/ros.h"
#include "std_msgs/Int32.h"
#include "geometry_msgs/Twist.h"

#include <sstream>

#define MAX_SPEED 150

std_msgs::Int32 msg_left;
std_msgs::Int32 msg_right;

ros::Publisher left_pub;
ros::Publisher right_pub; 

void speedCallback(const geometry_msgs::Twist& message)
{
   float x_vel = message.linear.x; //data from -.5 to .5
   float theta_vel = message.angular.z;

   int vel_L = 0;
   int vel_R = 0;

   if(theta_vel == 0){
     vel_L = MAX_SPEED * x_vel * 2;
     vel_R = MAX_SPEED * x_vel * 2;
    }else if(theta_vel > 0){ //going right
      vel_L = (MAX_SPEED * x_vel *2) - (MAX_SPEED * theta_vel * 2);
      vel_R = (MAX_SPEED * x_vel * 2);
    }else
    {
      theta_vel = theta_vel * -1;
      vel_L = (MAX_SPEED * x_vel * 2);
      vel_R = (MAX_SPEED * x_vel * 2) - (MAX_SPEED * theta_vel * 2);
    }
  msg_left.data = vel_L;
  msg_right.data = vel_R;

  left_pub.publish(msg_left);
  right_pub.publish(msg_right);
}


int main(int argc, char **argv)
{

  ros::init(argc, argv, "ratSpeed");

  ros::NodeHandle n;

  right_pub  = n.advertise<std_msgs::Int32>("motor_right", 1000);
  left_pub  = n.advertise<std_msgs::Int32>("motor_left", 1000);

  ros::Subscriber sub = n.subscribe("/cmd_vel", 1000, speedCallback);

  ros::Rate loop_rate(10);

  while(ros::ok())
  {
    ros::spinOnce();
    loop_rate.sleep();

  }


  return 0;
}
