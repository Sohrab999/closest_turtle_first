#!/usr/bin/env python3
import rclpy
import random
from rclpy.node import Node
from geometry_msgs.msg import Twist
from turtlesim.msg import Pose
from turtlesim.srv import Spawn
from functools import partial
class closest_turtle_first(Node):
    def __init__(self):
        super().__init__("spawn")
        self.timer=self.create_timer(1.0,self.call_sub)
        self.i=2
    def call_sub(self):
        # spawn in 7x7 grid so that my turtle doesnt get out of the way
        self.spawn(round(random.uniform(2.0, 9.0), 1),round(random.uniform(2.0, 9.0), 1),0.0,f"turtle{self.i}")
        self.i+=1
      
    def spawn(self,x,y,theta,name):
        client=self.create_client(Spawn,"/spawn")
        while not client.wait_for_service(1.0):
            self.get_logger().warn("waiting for services")
        request=Spawn.Request()
        request.x=x
        request.y=y
        request.theta=theta
        request.name=name
        future=client.call_async(request)
        future.add_done_callback(partial(self.spawn_call_back))
    def spawn_call_back(self,future):
        try:
            response=future.result()
        except Exception as e:
            self.get_logger().error("Something went wrong %r"%(e,))
        
        

def main(args=None):
    rclpy.init(args=args)
    node=closest_turtle_first()
    rclpy.spin(node)
    rclpy.shutdown()