#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
class circle(Node):
    def __init__(self):
        super().__init__("draw_circle")
        self.cmd_vel_publ=self.create_publisher(Twist,"/turtle1/cmd_vel",10)
        self.timer=self.create_timer(0.5,self.values)
        self.get_logger().info("draw a circle has started")

    def values(self):
        msg=Twist()
        msg.linear.x=2.0
        msg.angular.z=1.0
        self.cmd_vel_publ.publish(msg)
    

def main (args=None):
    rclpy.init(args=args)
    node=circle()
    rclpy.spin(node)
    rclpy.shutdown()
