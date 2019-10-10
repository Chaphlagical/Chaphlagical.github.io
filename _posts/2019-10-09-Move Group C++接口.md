---
bg: "2019-10-09.jpg"
layout: post
title:  "Move Group C++接口"
crawlertitle: "Move Group C++接口"
summary: "Move Group C++接口"
date:   2019-10-09 08:10:00 +0700
categories: posts
tags: ['Moveit!学习']
author: Chaf
---

本文介绍Moveit!中Move Group的C++接口

## 一、初始化

MoveIt在“planning groups”的一组关节上进行操作，并将它们存储在一个名为JointModelGroup的对象中。 在整个MoveIt中，术语“planning groups”和“joint model group”可互换使用。

```c++
static const std::string PLANNING_GROUP="panda_arm" 
```

初始化安装：

```c++
moveit::planning_interface::MoveGroupInterface move_group(PLANNING_GROUP);
```

我们将使用PlanningSceneInterface类在“虚拟世界”场景中添加和删除碰撞对象:

```c++
moveit::planning_interface::PlanningSceneInterface planning_scene_interface;
```

为了提升性能，常常使用指针组：

```c++
const robot_state::JointModelGroup* joint_model_group =
    move_group.getCurrentState()->getJointModelGroup(PLANNING_GROUP);
```

## 二、可视化

软件包MoveItVisualTools提供了许多功能，用于可视化RViz中的对象，机械手和轨迹以及调试工具。

```c++
namespace rvt = rviz_visual_tools;
moveit_visual_tools::MoveItVisualTools visual_tools("panda_link0");
visual_tools.deleteAllMarkers();
```

Remote control允许用户通过RViz中的按钮和键盘快捷键逐步浏览高级脚本

```c++
visual_tools.loadRemoteControl();
```

Rviz提供很多种类型的marker，这里使用文本、球体和圆柱体

```c++
Eigen::Isometry3d text_pose = Eigen::Isometry3d::Identity();
text_pose.translation().z() = 1.75;
visual_tools.publishText(text_pose, "MoveGroupInterface Demo", rvt::WHITE, rvt::XLARGE);
```

批量发布用于减少发送到RViz进行大型可视化的消息数量

```c++
visual_tools.trigger();
```

## 三、获得基本信息

打印参考组的名称：

```c++
ROS_INFO_NAMED("tutorial", "Planning frame: %s", move_group.getPlanningFrame().c_str());
```

打印末端执行器的名称：

```c++
ROS_INFO_NAMED("tutorial", "End effector link: %s", move_group.getEndEffectorLink().c_str());
```

打印机器人所有组：

```c++
ROS_INFO_NAMED("tutorial", "Available Planning Groups:");
std::copy(move_group.getJointModelGroupNames().begin(), move_group.getJointModelGroupNames().end(),
          std::ostream_iterator<std::string>(std::cout, ", "));
```

## 四、目标姿态规划

规划末端执行器的目标位姿：

```c++
geometry_msgs::Pose target_pose1;
target_pose1.orientation.w = 1.0;
target_pose1.position.x = 0.28;
target_pose1.position.y = -0.2;
target_pose1.position.z = 0.5;
move_group.setPoseTarget(target_pose1);
```

调取planner进行规划并进行可视化（非实际移动机器人）：

```c++
moveit::planning_interface::MoveGroupInterface::Plan my_plan;

bool success = (move_group.plan(my_plan) == moveit::planning_interface::MoveItErrorCode::SUCCESS);

ROS_INFO_NAMED("tutorial", "Visualizing plan 1 (pose goal) %s", success ? "" : "FAILED");
```

## 五、可视化规划

在Rviz中可视化规划轨迹

```c++
ROS_INFO_NAMED("tutorial", "Visualizing plan 1 as trajectory line");
visual_tools.publishAxisLabeled(target_pose1, "pose1");
visual_tools.publishText(text_pose, "Pose Goal", rvt::WHITE, rvt::XLARGE);
visual_tools.publishTrajectoryLine(my_plan.trajectory_, joint_model_group);
visual_tools.trigger();
visual_tools.prompt("Press 'next' in the RvizVisualToolsGui window to continue the demo");
```

## 六、控制机器人移动

```c++
move_group.move();
```

## 七、规划到一个关节空间中的目标

创建一个指向当前机器人状态的指针。RobotState为存储所有当前位置、速度、加速度数据的对象。

```c++
moveit::core::RobotStatePtr current_state = move_group.getCurrentState();
```

获得当前指定组当前的关节位置

```c++
std::vector<double> joint_group_positions;
current_state->copyJointGroupPositions(joint_model_group, joint_group_positions);
```

修改其中一个关节规划到新的关节空间并进行可视化

```c++
joint_group_positions[0] = -1.0;  // radians
move_group.setJointValueTarget(joint_group_positions);

success = (move_group.plan(my_plan) == moveit::planning_interface::MoveItErrorCode::SUCCESS);
ROS_INFO_NAMED("tutorial", "Visualizing plan 2 (joint space goal) %s", success ? "" : "FAILED");
```

在Rviz中可视化

```c++
visual_tools.deleteAllMarkers();
visual_tools.publishText(text_pose, "Joint Space Goal", rvt::WHITE, rvt::XLARGE);
visual_tools.publishTrajectoryLine(my_plan.trajectory_, joint_model_group);
visual_tools.trigger();
visual_tools.prompt("Press 'next' in the RvizVisualToolsGui window to continue the demo");
```





