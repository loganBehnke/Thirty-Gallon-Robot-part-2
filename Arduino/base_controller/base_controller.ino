#if defined(ARDUINO) && ARDUINO >= 100
  #include "Arduino.h"
#else
  #include <WProgram.h>
#endif

#define A_INPUT 3
#define B_INPUT
#define L_MOTOR_PWM 6
#define R_MOTOR_PWM 5 // random number change later
#define L_MOTOR_DIR 8
#define R_MOTOR_DIR 7 // random number change later

#include <math.h>
#include <ros.h>
#include <std_msgs/Int32.h>

ros::NodeHandle nh;

void set_left_motor(float speed)
{
  if(speed < 0)
  {
    digitalWrite(L_MOTOR_DIR, LOW);
    analogWrite(L_MOTOR_PWM, abs(speed));
  }else
  {
    digitalWrite(L_MOTOR_DIR, HIGH);
    analogWrite(L_MOTOR_PWM, speed);
  }
}

void set_right_motor(int speed)
{
   if(speed < 0)
  {
    digitalWrite(R_MOTOR_DIR, LOW);
    analogWrite(R_MOTOR_PWM, abs(speed));
  }else
  {
    digitalWrite(R_MOTOR_DIR, HIGH);
    analogWrite(R_MOTOR_PWM, speed);
  }
}

void left_motor_cb(const std_msgs::Int32& message)
{
  float speed = message.data;
  //set_left_motor(speed);
}

void right_motor_cb(const std_msgs::Int32& message)
{
  float speed = message.data;
  set_right_motor(speed);  
}

ros::Subscriber<std_msgs::Int32> left_sub("motor_left", &left_motor_cb);
ros::Subscriber<std_msgs::Int32> right_sub("motor_right", &right_motor_cb);

void setup() {
  // put your setup code here, to run once:
  nh.initNode();
  nh.subscribe(left_sub);
  nh.subscribe(right_sub);

  pinMode(R_MOTOR_PWM, OUTPUT);
  pinMode(R_MOTOR_DIR, OUTPUT);


}

void loop() {
  // put your main code here, to run repeatedly:
  //critical section
  //noInterrupts();
  nh.spinOnce();
  //interrupts();
  
  delay(1);
}
