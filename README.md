# Robot Assisted Tours (RAT)

to install this package 

first delete the build and devel folders

run

```
git submodule init
```

then run

```
rosdep install --from-paths src --ignore-src --rosdistro kinetic -y
```

you should get an out put of

```
#All required rosdeps installed successfully
```

then run 

```
catkin_make
```
