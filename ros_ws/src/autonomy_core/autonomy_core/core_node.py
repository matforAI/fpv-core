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
from autonomy_core.return_home import ReturnHome

from autonomy_core.behavior_tree import (
    Status,
    Condition,
    Action,
    Selector,
    Sequence
)


class AutonomyCore(Node):

    def __init__(self):
        super().__init__("autonomy_core")

        self.create_subscription(String, "/detections", self.on_detection, 10)
        self.create_subscription(Odometry, "/odometry/filtered", self.on_odom, 10)

        self.cmd_pub = self.create_publisher(Twist, "/cmd_vel_autonomy", 10)
        self.health_pub = self.create_publisher(String, "/core/health", 10)

        self.mission = MissionManager(self)
        self.tracker = TargetTracker(640)
        self.failsafe = FailSafe()
        self.health = HealthMonitor()
        self.blackbox = BlackBox()
        self.rth = ReturnHome()

        self.goal_sent = False
        self.cmd = Twist()

        # -------- Behavior Tree --------
        self.bt = Selector([
            # FAIL → RETURN HOME
            Sequence([
                Condition(lambda: not self.failsafe.odom_ok()),
                Action(self.return_home)
            ]),

            # TRACK TARGET
            Sequence([
                Condition(lambda: self.failsafe.detection_alive()),
                Action(self.track_target)
            ]),

            # NAVIGATION
            Action(self.navigate)
        ])

        self.timer = self.create_timer(0.1, self.loop)

        self.get_logger().info("AUTONOMY CORE + RETURN HOME ONLINE")

    # ---------------- callbacks ----------------

    def on_detection(self, msg):
        try:
            cx, _, _, _ = msg.data.split(",")
            self.tracker.update_bbox(float(cx))
            self.failsafe.update_detection()
        except:
            pass

    def on_odom(self, msg):
        self.failsafe.update_odom()
        self.rth.update_home(msg)

    # ---------------- BT ACTIONS ----------------

    def return_home(self):
        home = self.rth.get_home()
        if home:
            self.mission.send_goal(home[0], home[1])
            self.blackbox.log("RTH", f"{home}")
        self.cmd.linear.x = 0.0
        self.cmd.angular.z = 0.0

    def track_target(self):
        err = self.tracker.get_yaw_error()
        self.cmd.linear.x = 0.0
        self.cmd.angular.z = -err * 1.2
        self.blackbox.log("BT", "TRACK")

    def navigate(self):
        if not self.goal_sent:
            self.mission.send_goal(5.0, 0.0)
            self.goal_sent = True
        self.cmd.linear.x = 0.0
        self.cmd.angular.z = 0.0
        self.blackbox.log("BT", "NAV")

    # ---------------- LOOP ----------------

    def loop(self):

        self.health.tick()
        self.cmd = Twist()

        self.bt.tick()

        self.cmd_pub.publish(self.cmd)

        self.health_pub.publish(
            String(data=json.dumps(self.health.get()))
        )


def main():
    rclpy.init()
    node = AutonomyCore()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()
