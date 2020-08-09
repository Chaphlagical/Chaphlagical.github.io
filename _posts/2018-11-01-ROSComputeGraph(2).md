---
layout: post
title: ROS Computation Graph(2)
subtitle: ROS Learning (3)
thumbnail-img: /assets/images/thumbnail-img/ROS.jpg
cover-img: /assets/images/cover-img/ROS.jpg
tags: [Robotics, ROS]
readtime: true
comments: true
---

介绍如何创建主题和编写主题发布者和主题订阅者程序

#### 1、创建功能包

在catkin_ws工作空间中创建一个新的功能包my_topic_test：

```shell
$ cd ~/catkin_ws
$ source devel/setup.bash
$ cd ~/catkin_ws/src
$ catkin_create_pkg my_topic_test std_msgs rospy roscpp
```

然后编译新建的my_topic_test功能包：

```shell
$ cd ~/catkin_ws
$ catkin_make
```

#### 2、编写主题发布者程序

基本步骤：

**1、初始化ROS节点**

**2、定义主题发布者：主题名、消息类型、消息队列的长度**

**3、将消息发布到主题上**

示例：

在~/catkin_ws/src/my_topic/src目录下新建talker.cpp文件：

```c++
#include "ros/ros.h"//包含ROS命令的头文件
#include "std_msgs/String.h"//创建String消息过程中出现的，包含有消息类型
#include <sstream>

int main(int argc,char**argv){
    ros::init(argc,argv,"talker");//节点初始化，“talker”为节点名称
    ros::NodeHandle n;//创建用于处理该节点的句柄
    ros::Publisher my_pub = n.advertise<std_msgs::String>("my_topic",100);
    //定义节点发布者，主题名为“my_topic”，发布到该主题的消息类型为std_msgs::String，100为发布队列		的长度
    ros::Rate loop_rate(1);//消息发布频率
    int cnt = 1;
    std::msgs::String msg;
    while(ros::ok()){//按键Ctrl+C跳出循环
        std::stringstream ss;
        if((cnt%2)==0) ss << "false";
        else ss << "true";
        msg.data = ss.str();//赋值
        ROS_INFO("%s",msg.data.c_str());//将数据显示在命令行窗口
        my_pub.publish(msg);//发布消息到主题上
        loop_rate.sleep();//程序休眠，使次序循环频率为1Hz
        cnt = cnt*3+1;
    }
    return 0;
}
```

或者新建talk.py文件：

```python
#！/user/bin/env python
import rospy#调用ROS
from std_msgs.msg import String
rospy.init_node('talker')#初始化，节点名称“talker”
def talker():
    my_pub = rospy.Publisher('my_topic', String)#定义发布者“”
    r = rospy.Rate(1)
    cnt = 1
    while not rospy.is_shutdown():
        if(cnt%2) ==0 :
            str = "false"
        else:
            str = "true"
        rospy.loginfo(str)
        my_pub.publish(String(str))
        cnt = cnt*3 + 1
        r.sleep()
        
if __name__ == '__main__':
    try:
        talker()
    except rospy.ROSInterruptException:
        pass 
```



#### 3、编写主题订阅者程序 

在~/catkin_ws/src/my_topic/src目录下新建listener.cpp文件： 

```c++
# include "ros/ros.h"
# include "std_msgs/String.h"

void MyTopicCallback(const std_msgs::String::ConstPtr& msg){//回调函数
    ROS_INFO("I heard:[%s]",msg->data.c_str());
}

int main(int argc, char**argv){
    ros::init(argc,argv,"listener");//初始化
    ros::NodeHandle n;//定义句柄
    ros::Subscriber my_pub = n.subscribe("my_topic",100,MyTopicCallback);//定义订阅者
    ros::spin();//进入消息处理循环，Ctrl+C可跳出循环
    return 0;    
}
```

或者新建talk.py文件：

```python
#! /user/bin/env python
import ros
from std_msgs.msg import String
def callback(data)://回调函数
    rospy.loginfo(rospy.get_call_id()+"I heard %s",data.data)

def listener():
    rospy.init_node('listener', anonymous = True)//初始化
    rospy.Subscriber('my_topic',String,callback)//定义订阅者
    rospy.spin()//消息循环
    
if __name__ == '__main__':
    listener()
```

#### 4、运行ROS节点

##### （1）C++

打开~/catkin_ws/src/my_topic_test文件夹下的CMakeLists.txt文件，并添加如下代码：

```
add_executable(talker src/talker.cpp)
target_link_libraries(talker ${catkin_LIBRARIES})
add_dependencies(talker my_topic_test_generate_message_cpp)

add_executable(listener src/listener.cpp)
target_link_libraries(listener ${catkin_LIBRARIES})
add_dependencies(listener my_topic_test_generate_message_cpp)
```

保存CMakeLists.txt文件，重新编译功能包：

```shell
$ cd ~/catkin_ws/
$ catkin_make
```

编译成功后，需要重新配置setup.bash：

```shell
$ cd ~/catkin_ws
$ source devel/setup.bash
```

启用roscore，重新打开两个终端分别输入rosrun my_topic_test talker和rosrun my_topic_test listener即可运行节点

##### （2） Python

将.py文件转为可执行文件：

```shell
$ roscd my_topic_test
$ chmod +x src/talker.py
$ chmod +x src/listener.py
```

在两个终端分别运行：

```shell
$ rosrun my_topic_test talker.py
$ rosrun my_topic_test listener.py
```

