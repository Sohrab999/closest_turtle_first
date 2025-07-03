#!/usr/bin/env python3
import rclpy
import random
import math
from rclpy.node import Node
from geometry_msgs.msg import Twist
from turtlesim.msg import Pose
from turtlesim.srv import Spawn
from functools import partial
from std_srvs.srv import Empty
from turtlesim.srv import Kill

class closest_turtle_first(Node):
    def __init__(self):
        super().__init__("closest_turtle_first")
        self.timer=self.create_timer(0.5,self.spawn_funtion)
        self.i=0       #this is the number for the turtles i spawn
        self.indx=-1   #this is the index of the nearest turtle
        self.goal_x=None     #these are the coordinates
        self.goal_y=None
        self.msg_t1=None
        self.pose:dict[int,tuple[float,float]]={}   #this stores my coordinates

        #this stores the displacement of the turtle1 from the spawning turtles
        self.dist: dict[int, float] = {}           
        self.a=0
        self.b=0
        self.pub=self.create_publisher(Twist,"/turtle1/cmd_vel",10)
        self.sub=self.create_subscription(Pose,"/turtle1/pose",self.call_sub,10)
    def call_sub(self,msg:Pose):
        self.msg_t1=msg
        #updating the displacement of turtle1 to spawning turtles
        for k, (d, e) in self.pose.items():
            self.dist[k] = math.sqrt((d - self.msg_t1.x)**2 + (e - self.msg_t1.y)**2)
        if not self.dist:
            return
        #to find the index of the nearest turtle
        self.indx = min(self.dist, key=self.dist.get)

        self.goal_x,self.goal_y=self.pose[self.indx]
        
        tv= Twist()
        dx, dy  = self.goal_x - self.msg_t1.x, self.goal_y - self.msg_t1.y
        distance = math.hypot(dx, dy)
        desired  = math.atan2(dy, dx)
        angle_error = math.atan2(
            math.sin(desired - self.msg_t1.theta),
            math.cos(desired - self.msg_t1.theta)
        )
        if abs(angle_error)>0.1:
            tv.angular.z=5.0*angle_error
        if distance>0.2:
            tv.linear.x=3.5*distance
        self.pub.publish(tv)

        if distance<0.5:
            self.clear()
            self.pose.pop(self.indx,None)
            self.dist.pop(self.indx,None)
            self.kill(f"spawned_turtle{self.indx}")
    def spawn_funtion(self):
        if self.msg_t1 is None:
            return
        
        # spawn in 7x7 grid so that my turtle doesnt get out of the way
        self.a=round(random.uniform(2.0, 9.0), 1)
        self.b=round(random.uniform(2.0, 9.0), 1)
        self.spawn(self.a,self.b,0.0,f"spawned_turtle{self.i}")
        # self.dist.append(math.sqrt((self.a - self.msg_t1.x)**2 + (self.b - self.msg_t1.y)**2)) # problem
        self.dist[self.i] = math.sqrt((self.a - self.msg_t1.x)**2 + (self.b - self.msg_t1.y)**2)
        # self.dist.append(math.sqrt((self.a - self.msg_t1.x)**2 + (self.b - self.msg_t1.y)**2))

        # coordinates of my spawned  turtle
        self.pose[self.i]=(self.a,self.b)
        self.i +=1


    #service for spawn
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


    #service for clear
    def clear(self):
        client_clear=self.create_client(Empty,"/clear") 
        request_clear=Empty.Request()
        future_clear=client_clear.call_async(request_clear)
        future_clear.add_done_callback(partial(self.clear_call_back))
    def clear_call_back(self,future_clear):
        try:
            response=future_clear.result()
        except Exception as e:
            self.get_logger().error("Something went wrong %r"%(e,))


    #service for kill
    def kill(self,name):
        client_kill=self.create_client(Kill,"/kill")
        request_kill=Kill.Request()
        request_kill.name=name
        future_kill=client_kill.call_async(request_kill)
        future_kill.add_done_callback(partial(self.kill_call_back))
    def kill_call_back(self,future_kill):
        try:
            response=future_kill.result()
        except Exception as e:
            self.get_logger().error("Something went wrong %r"%(e,))

def main(args=None):
    rclpy.init(args=args)
    node=closest_turtle_first()
    rclpy.spin(node)
    rclpy.shutdown()