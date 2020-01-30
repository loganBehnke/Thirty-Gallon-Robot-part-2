# Robot Assisted Tours (RAT)

To set up a virtual macheine follow the steps in [this file](SettingUpLinuxAndROS.pdf)

To install this package 

run

```
rosdep install --from-paths src --ignore-src --rosdistro kinetic -y
```

You should get an out put of

```
#All required rosdeps installed successfully
```

Then run 

```
catkin_make
```

Install openni_launch
```
sudo apt install ros-kinetic-openni-launch
```

To run our tech demo first you need to source ros in the catkin_ws
```
source devel/setup.bash
roslaunch src/mapping.launch
```