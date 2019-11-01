---
title: Moveit!与Rviz可视化
tags: Moveit!
article_header:
  type: cover
  image:
    src: /assets/images/Moveit.jpg
---

使用Rviz可视化Moveit!机械臂控制入门

## 一、启动Demo与配置插件

运行Demo：

```powershell
roslaunch panda_moveit_config demo.launch rviz_tutorial:=true
```

将会看到Rviz中的空白世界：

![](http://docs.ros.org/kinetic/api/moveit_tutorials/html/_images/rviz_empty.png)

添加"MotionPlanning"项：

![](http://docs.ros.org/kinetic/api/moveit_tutorials/html/_images/rviz_plugin_motion_planning_add.png)

将会看到机器人出现在Rviz中：

![](http://docs.ros.org/kinetic/api/moveit_tutorials/html/_images/rviz_start.png)

* 在“Global Options” 中的“Displays”选项, 设置 **Fixed Frame** 为 `/panda_link0`
* 设置“MotionPlanning”中的选项：
  - Make sure the **Robot Description** field is set to `robot_description`.
  - Make sure the **Planning Scene Topic** field is set to `/planning_scene`.
  - In **Planning Request**, change the **Planning Group** to `panda_arm`.
  - In **Planned Path**, change the **Trajectory Topic** to `/move_group/display_planned_path`.

## 二、与可视化机器人操作

四种不同的可视化活动：

1. 运动规划的开始状态（计划组显示为绿色）
2. 运动规划的目标状态（计划组显示为橙色）。
3. 在规划场景/规划环境机器人的配置
4. 机器人的规划路径

状态的显示可以在复选框内选择：

1. 在“Planning Request” 选项卡，开始状态使用“Query Start State”复选框
2. 在“Planning Request” 选项卡，目标状态使用“Query Goal State”复选框
3. 在 “Scene Robot”选项卡，规划场景机器人使用“Show Scene Robot”复选框
4. 在“Planned Path” 选项卡，规划路径使用“Show Robot Visual”复选框

![](http://docs.ros.org/kinetic/api/moveit_tutorials/html/_images/rviz_plugin_visualize_robots.png)

## 三、与机器人交互

### 1、移动至发生碰撞

关节将变红

![](http://docs.ros.org/kinetic/api/moveit_tutorials/html/_images/rviz_plugin_collision.png)

使用"Use Collision-Aware IK"复选框允许您切换IK解算器的行为。当复选框打勾，求解器将试图找到一个理想的末端执行器的位姿自由冲突的解决。当它未打勾，求解器将允许发生碰撞。在碰撞环节始终还是会显示红色。

![](http://docs.ros.org/kinetic/api/moveit_tutorials/html/_images/rviz_plugin_collision_aware_ik_checkbox.png)

### 2、移动到不可达区域

![](http://docs.ros.org/kinetic/api/moveit_tutorials/html/_images/rviz_plugin_invalid.png)

## 四、使用MotionPlanning

对机器人进行轨迹规划：

- 移动开始状态到希望的位置
- 移动目标状态到另一个希望的位置
- 确保状态不会与机器人产生冲突
- 确保路径规划能可视化，在Planned Path选项卡上检查“Show Trail”复选框

在Motion Planning的planning选项卡，按下Plan 按钮，应该看到手臂移动并显示它的轨迹。

![](http://docs.ros.org/kinetic/api/moveit_tutorials/html/_images/rviz_plugin_planned_path.png)

