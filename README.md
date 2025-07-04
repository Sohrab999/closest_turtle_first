# 🐢 closest_turtle_first

This is my first ROS 2 project using the `turtlesim` simulator. The goal of the project is to identify the closest turtle from a set of spawned turtles and make the main turtle move toward it.

---

## 🚀 Features

- Learn basic ROS 2 concepts: Nodes, Publishers, Subscribers, and Services  
- Automatically spawn multiple turtles in turtlesim  
- Calculate and target the closest turtle in real-time  
- Demonstrates inter-node communication and simple decision logic

---

## 🛠️ Requirements

- ROS 2 (Tested on [Humble/Jazzy])  
- Python 3  
- `turtlesim` package (comes pre-installed with ROS 2 demos)

---

## 📁 Project Structure

closest_turtle_first/
├── closest_turtle_first/
│ ├── init.py
│ ├── closest_turtle_first.py # Main script that implements the logic
│ ├── spawn_turtles.py # Spawns multiple turtles
│ └── basic_* # Practice scripts for publisher, subscriber, and service
├── package.xml
└── setup.py


---

## ▶️ How to Run

1. **Source your ROS 2 environment:**
   ```bash
   source /opt/ros/<your_ros2_distro>/setup.bash

2. Build the workspace:
  colcon build

3. Source your workspace:
   source install/setup.bash

4.Launch turtlesim node (in a new terminal):
  ros2 run turtlesim turtlesim_node

5.Run your script:
  ros2 run closest_turtle_first closest_turtle_first

## 📚 What I Learned
Fundamentals of ROS 2

Creating custom Python nodes

Using services to spawn turtles dynamically

Subscribing to pose data and computing distances

Writing modular and reusable ROS 2 code

## 🧠 Future Improvements
Add visualization of target paths

Extend to 3D turtlesim or Gazebo environments

Improve performance for higher number of turtles

Implement obstacle avoidance logic

