#!/usr/bin/env python3
import rclpy
import math
import sys
from rclpy.node import Node
from geometry_msgs.msg import Twist
from turtlesim.msg import Pose
class Go_to_goal(Node):
    def __init__(self,x:float,y:float):
        super().__init__("go_to_goal")
        self.x=x
        self.y=y
        self.pose=None
        self.pub=self.create_publisher(Twist,"/turtle1/cmd_vel",10)
        self.sub=self.create_subscription(Pose,"/turtle1/pose",self.position,10)
        self.timer=self.create_timer(0.1,self.go)
    def position(self,msg:Pose):
        self.pose=msg
    def go(self):
        if self.pose is None:
            return
           
        tv= Twist()
        dx,dy=self.x-self.pose.x,self.y-self.pose.y
        distance=math.hypot(dx,dy)
        desired=math.atan2(dy,dx)
        angle_error=math.atan2(math.sin(desired-self.pose.theta),math.cos(desired-self.pose.theta))
        if abs(angle_error)>0.1:
            tv.angular.z=3.5*angle_error
        if distance>0.2:
            tv.linear.x=3.5*distance
        self.pub.publish(tv)
def main(args=None):
    rclpy.init(args=args)
    if len(sys.argv) != 3:
        print("USAGE: ros2 run my_pkg go_to_goal <x> <y>")
        return
    x = float(sys.argv[1])
    y = float(sys.argv[2])
    node=Go_to_goal(x,y)
    rclpy.spin(node)
    rclpy.shutdown()
if __name__=="__main__":
    main()