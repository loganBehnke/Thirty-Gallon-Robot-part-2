#if defined(ARDUINO) && ARDUINO >= 100
  #include "Arduino.h"
#else
  #include <WProgram.h>
#endif

#include <math.h>
#include <ros.h>
#include <geometry_msgs/Twist.h>

ros::NodeHandle nh;

const float WHEEL_DIST = 10.16; //centimeters

int L_motor_back = 9;
int L_motor_go = 5;
int R_motor_go = 6;
int R_motor_back = 10;

void set_L_motor_speed(int speed){

    //going backwards
    if(speed < 0){
       speed = speed * (-1);
       digitalWrite(L_motor_go, LOW);
       digitalWrite(L_motor_back, HIGH);
       analogWrite(L_motor_back, speed);
    }else if(speed > 0){
      digitalWrite(L_motor_go, HIGH);
      digitalWrite(L_motor_back, LOW);
      analogWrite(L_motor_go, speed);
    }else{
      digitalWrite(L_motor_go, LOW);
      digitalWrite(L_motor_back, LOW);
      analogWrite(L_motor_go, 0);
      analogWrite(L_motor_back, 0);
    }
  
}

void set_R_motor_speed(int speed){

    //going backwards
    if(speed < 0){
       speed = speed * (-1);
       digitalWrite(R_motor_go, LOW);
       digitalWrite(R_motor_back, HIGH);
       analogWrite(R_motor_back, speed);
    }else if(speed > 0){
      digitalWrite(R_motor_go, HIGH);
      digitalWrite(R_motor_back, LOW);
      analogWrite(R_motor_go, speed);
    }else{
      digitalWrite(R_motor_go, LOW);
      digitalWrite(R_motor_back, LOW);
      analogWrite(R_motor_go, 0);
      analogWrite(R_motor_back, 0);
    }
  
}

void messageCb(const geometry_msgs::Twist& message){
    //Deal with message
    float x_vel = message.linear.x * 2; //data from -.5 to .5
    float theta_vel = message.angular.z * 2;

    int vel_L = 0;
    int vel_R = 0;

    if(theta_vel == 0){
      vel_L = 255 * x_vel * 2;
      vel_R = 255 * x_vel * 2;
    }else if(theta_vel > 0){ //going right
      vel_L = (255 * x_vel *2) - (255 * theta_vel * 2);
      vel_R = (255 * x_vel * 2);
    }else{
      theta_vel = theta_vel * -1;
      vel_L = (255 * x_vel * 2);
      vel_R = (255 * x_vel * 2) - (255 * theta_vel * 2);
    }
    
    //int vel_L = (theta_vel*WHEEL_DIST)/2 + x_vel;
    //int vel_R = x_vel*2 - vel_L;

    //vel_L = round(vel_L * 255);
    //vel_R = round(vel_R * 255);

    //Serial.print(vel_L);
    //Serial.print(vel_R);

    set_L_motor_speed(vel_L);
    set_R_motor_speed(vel_R);
    
}

ros::Subscriber<geometry_msgs::Twist> sub("/cmd_vel", &messageCb);

void setup() {
  // put your setup code here, to run once:
  pinMode(L_motor_back, OUTPUT);
  pinMode(L_motor_go, OUTPUT);
  pinMode(R_motor_go, OUTPUT);
  pinMode(R_motor_back, OUTPUT);

  nh.initNode();
  nh.subscribe(sub);
  
}

void loop() {
  // put your main code here, to run repeatedly:
  nh.spinOnce();
  delay(1);

}
