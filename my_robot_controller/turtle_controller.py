#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
from turtlesim.msg import Pose
class controller(Node):
    def __init__(self):
        super().__init__("turtle_controller")
        self.pub=self.create_publisher(Twist,"/turtle1/cmd_vel",10)
        self.sub=self.create_subscription(Pose,"/turtle1/pose",self.position,10)
    def position(self,msg:Pose):
        p=Twist()
        if msg.x<3.0 or msg.x>8.0 or msg.y<3.0 or msg.y>8.0:
            p.linear.x=1.0
            p.angular.z=1.0
        else:        
            p.linear.x=1.0
            p.angular.z=0.0
        self.pub.publish(p)

def main(args=None):
    rclpy.init(args=args)
    node=controller()
    rclpy.spin(node)
    rclpy.shutdown()