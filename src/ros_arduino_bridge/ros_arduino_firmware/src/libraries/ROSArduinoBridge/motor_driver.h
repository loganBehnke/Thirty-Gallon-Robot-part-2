/***************************************************************
   Motor driver function definitions - by James Nugen
   *************************************************************/

#ifdef L298_MOTOR_DRIVER
  #define RIGHT_MOTOR_DIR 5
  #define LEFT_MOTOR_DIR  6
  #define RIGHT_MOTOR_PWM  9
  #define LEFT_MOTOR_PWM   10
#endif

void initMotorController();
void setMotorSpeed(int i, int spd);
void setMotorSpeeds(int leftSpeed, int rightSpeed);
