#!/usr/bin/env python3

import rclpy
from rclpy.node import Node

from geometry_msgs.msg import Twist
from nav_msgs.msg import Odometry
from std_msgs.msg import String

from autonomy_core.state_machine import StateMachine, State
from autonomy_core.mission_manager import MissionManager
from autonomy_core.target_tracker import TargetTracker


class AutonomyCore(Node):

    def __init__(self):
        super().__init__("autonomy_core")

        self.create_subscription(
            String,
            "/detections",
            self.on_detection,
            10
        )

        self.create_subscription(
            Odometry,
            "/odometry/filtered",
            self.on_odom,
            10
        )

        self.cmd_pub = self.create_publisher(
            Twist,
            "/cmd_vel_autonomy",
            10
        )

        self.sm = StateMachine()
        self.mission = MissionManager(self)
        self.tracker = TargetTracker(image_width=640)

        self.has_detection = False
        self.odom_ok = False
        self.goal_sent = False

        self.timer = self.create_timer(0.1, self.loop)

        self.get_logger().info("AUTONOMY CORE + TRACKING ONLINE")

    def on_detection(self, msg):
        try:
            cx, cy, w, h = msg.data.split(",")
            self.tracker.update_bbox(float(cx))
            self.has_detection = True
        except:
            self.has_detection = False

    def on_odom(self, msg):
        self.odom_ok = True

    def loop(self):

        state = self.sm.update(
            has_detection=self.has_detection,
            odom_ok=self.odom_ok
        )

        cmd = Twist()

        # ───────────────
        # NAVIGATION MODE
        # ───────────────
        if state == State.MOVE:
            if not self.goal_sent:
                self.mission.send_goal(5.0, 0.0)
                self.goal_sent = True

        # ───────────────
        # TRACKING MODE
        # ───────────────
        if state == State.HOLD:
            yaw_error = self.tracker.get_yaw_error()
            cmd.angular.z = -yaw_error * 1.2
            cmd.linear.x = 0.0

        # ───────────────
        # FAILSAFE
        # ───────────────
        if state == State.FAIL:
            cmd.linear.x = 0.0
            cmd.angular.z = 0.0

        self.cmd_pub.publish(cmd)


def main():
    rclpy.init()
    node = AutonomyCore()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()
