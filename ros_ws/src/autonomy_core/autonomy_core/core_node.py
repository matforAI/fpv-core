#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from std_msgs.msg import String
from geometry_msgs.msg import Twist
from nav_msgs.msg import Odometry
import json

from autonomy_core.state_machine import StateMachine, State
from autonomy_core.mission_manager import MissionManager
from autonomy_core.target_tracker import TargetTracker
from autonomy_core.failsafe import FailSafe
from autonomy_core.health_monitor import HealthMonitor
from autonomy_core.blackbox import BlackBox


class AutonomyCore(Node):

    def __init__(self):
        super().__init__("autonomy_core")

        # subs
        self.create_subscription(String, "/detections", self.on_detection, 10)
        self.create_subscription(Odometry, "/odometry/filtered", self.on_odom, 10)

        # pubs
        self.cmd_pub = self.create_publisher(Twist, "/cmd_vel_autonomy", 10)
        self.health_pub = self.create_publisher(String, "/core/health", 10)

        # modules
        self.sm = StateMachine()
        self.mission = MissionManager(self)
        self.tracker = TargetTracker(640)
        self.failsafe = FailSafe()
        self.health = HealthMonitor()
        self.blackbox = BlackBox()

        self.goal_sent = False
        self.timer = self.create_timer(0.1, self.loop)

        self.get_logger().info("AUTONOMY CORE FULL SYSTEM ONLINE")

    def on_detection(self, msg):
        try:
            cx, _, _, _ = msg.data.split(",")
            self.tracker.update_bbox(float(cx))
            self.failsafe.update_detection()
        except:
            pass

    def on_odom(self, msg):
        self.failsafe.update_odom()

    def loop(self):

        self.health.tick()

        odom_ok = self.failsafe.odom_ok()
        det_ok = self.failsafe.detection_alive()

        state = self.sm.update(det_ok, odom_ok)

        cmd = Twist()

        # NAVIGATION
        if state == State.MOVE:
            if not self.goal_sent:
                self.mission.send_goal(5.0, 0.0)
                self.goal_sent = True

        # TRACKING
        if state == State.HOLD:
            yaw_error = self.tracker.get_yaw_error()
            cmd.angular.z = -yaw_error * 1.2

        # FAILSAFE
        if state == State.FAIL:
            cmd.linear.x = 0.0
            cmd.angular.z = 0.0

        self.cmd_pub.publish(cmd)

        # health topic
        self.health_pub.publish(
            String(data=json.dumps(self.health.get()))
        )

        # blackbox log
        self.blackbox.log("state", state.name)


def main():
    rclpy.init()
    node = AutonomyCore()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()
