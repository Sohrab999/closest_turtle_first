#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist 
from turtlesim.msg import Pose
from turtlesim.srv import SetPen
from functools import partial
class controller(Node):
    def __init__(self):
        super().__init__("turtle_controller_service")
        self.prevx=0
        self.pub=self.create_publisher(Twist,"/turtle1/cmd_vel",10)
        self.sub=self.create_subscription(Pose,"/turtle1/pose",self.call_sub,10)
    def call_sub(self,msg:Pose):
        cv=Twist()
        if(msg.x>8.0 or msg.x<3.0 or msg.y>8.0 or msg.y<3.0):
            cv.linear.x=1.0
            cv.angular.z=1.0
        else:
            cv.linear.x=1.0
            cv.angular.z=0.0
        self.pub.publish(cv)
        if msg.x>5.5 and self.prevx<=5.5:
            self.prevx=msg.x
            self.get_logger().info("set colour to red")
            self.call_setpen_ser(255,0,0,3,0)
        elif msg.x<=5.5 and self.prevx>5.5:
            self.prevx=msg.x
            self.get_logger().info("set colour to green")
            self.call_setpen_ser(0,255,0,3,0)
    def call_setpen_ser(self,r,g,b,width,off):
        client=self.create_client(SetPen,"/turtle1/set_pen")
        while not client.wait_for_service(0.001):
            self.get_logger().warn("waiting for service")
        request=SetPen.Request()
        request.r=r
        request.g=g
        request.b=b
        request.width=width
        request.off=off
        future=client.call_async(request)
        future.add_done_callback(partial(self.call_setpen))
    def call_setpen(self,future):
        try:
            response=future.result()
        except Exception as e:
            self.get_logger().error("something went wrong %r"%(e,))

def main(args=None):
    rclpy.init(args=args)
    node=controller()
    rclpy.spin(node)
    rclpy.shutdown()