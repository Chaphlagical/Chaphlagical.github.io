---
layout: post
title: Ros File System
subtitle: ROS Learning (1)
thumbnail-img: /assets/images/thumbnail-img/ROS.jpg
cover-img: /assets/images/cover-img/ROS.jpg
tags: [Robotics, ROS]
readtime: true
comments: true
---

Ros File System

## 一、设置ROS环境变量

在安装好ROS之后，在正式使用ROS之前，我们需要配置ROS的环境变量，我们可以在每次使用之前键入命令

```shell
$ source /opt/ros/<distro>/setup.bash
```

或者在第一次使用时键入

```shell
$ echo "source /opt/ros/<distro>/setup.bash" >> ~/.bashrc
$ source ~/.bashrc
```

每次打开终端自动配置环境变量。

为检验环境变量是否配置完成，可以通过命令：

```shell
$ printenv | grep ROS
```

若出现类似

```
ROS_ETC_DIR=/opt/ros/melodic/etc/ros
ROS_ROOT=/opt/ros/melodic/share/ros
ROS_MASTER_URI=http://localhost:11311
ROS_VERSION=1
ROS_PYTHON_VERSION=2
ROS_PACKAGE_PATH=/opt/ros/melodic/share
ROSLISP_PACKAGE_DIRECTORIES=
ROS_DISTRO=melodic
```

说明配置成功。

## 二、创建工作空间

ROS的工作空间有两种：rosbuild和catkin，其中catkin适用于groovy及以后的版本，这里介绍catkin工作空间的创建。

#### 1、创建空的catkin工作空间

```shell
$ mkdir -p ~/catkin_ws/src
$ cd ~/catkin_ws/src
$ catkin_init_workspace
```

#### 2、编译工作空间

```shell
$ cd ~/catkin_ws/
$ catkin_make
```

执行命令后，~/catkin_ws/目录下会产生build和devel两个文件夹。其中devel包含几个setup.*sh文件。

#### 3、更新环境变量

```shell
$ source devel/setup.bash
```

至此工作空间创建完毕

## 三、创建功能包

ROS功能包同样分rosbuild和catkin功能包，这里介绍catkin功能包。

#### 1、创建功能包

首先将ROS当前的工作空间设为catkin_ws：

```shell
$ cd ~/catkin_ws/
$ source devel/setup.bash
```

然后在~/catkin_ws/src路径下创建beginner_tutorials功能包：

```shell
$ cd ~/catkin_ws/src
$ catkin_create_pkg beginner_tutorials std_msgs rospy roscpp
```

这里，catkin_create_pkg语句原型为

```shell
$ catkin_create_pkg <package_name> [depend1] [depend2] [depend3]
```

#### 2、编译功能包

```shell
$ cd ~/catkin_ws/
$ catkin_make
```

上述命令将编译工作空间中所有的功能包，若想编译单独某个包，可运行命令：

```shell
$ cd ~/catkin_ws/
$ catkin_make --pkg package_name
```

## 四、文件系统中常用的命令

#### 1、rospack

```shell 
$ rospack find [package_name]
```

将会返回功能包的地址

#### 2、roscd

```shell 
$ roscd [locationname][/subdir]
```

将目录定位到.../subdir

#### 3、rosls

```shell
$ rosls [locationname][/subdir]
```

列出.../subdir下的所有文件和目录

#### 4、catkin_create_pkg

```shell
$ catkin_create_pkg <package_name> [depend1][depend2] [depend3]
```

创建功能包

#### 5、catkin_make

```shell
$ catkin_make
```

编译工作空间

#### 6、rosdep

```shell
$ rosdep <packagename>
```

安装功能包的系统依赖项

#### 7、 rqt_dep

查看包的依赖关系

#### 8、 roscp

复制文件

#### 9、rosd

列出功能包的目录

#### 10、rosed

编辑文件