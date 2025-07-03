#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from turtlesim.msg import Pose

class PoseSubscriber(Node):
    def __init__(self):
        super().__init__("pose_subscriber")
        self.sub=self.create_subscription(Pose,"/turtle1/pose",self.position,10)

    def position(self,msg: Pose):
        self.get_logger().info("(" + str(msg.x) + "," + str(msg.y) + ")")

def main(args=None):
    rclpy.init(args=args)
    node=PoseSubscriber()
    rclpy.spin(node)
    rclpy.shutdown()