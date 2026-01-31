#!/usr/bin/env python3

import rclpy
from rclpy.node import Node

from geometry_msgs.msg import Twist
from nav_msgs.msg import Odometry
from std_msgs.msg import String

from autonomy_core.state_machine import StateMachine, State
from autonomy_core.mission_manager import MissionManager


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

        self.has_detection = False
        self.odom_ok = False

        self.sm = StateMachine()
        self.mission = MissionManager(self)

        self.goal_sent = False

        self.timer = self.create_timer(0.2, self.loop)

        self.get_logger().info("AUTONOMY CORE ONLINE")

    def on_detection(self, msg):
        self.has_detection = True

    def on_odom(self, msg):
        self.odom_ok = True

    def loop(self):

        state = self.sm.update(
            has_detection=self.has_detection,
            odom_ok=self.odom_ok
        )

        # если разрешено движение — отправляем миссию
        if state == State.MOVE and not self.goal_sent:
            self.mission.send_goal(5.0, 0.0)
            self.goal_sent = True

        cmd = Twist()

        if state == State.MOVE:
            cmd.linear.x = 0.0   # Nav2 рулит сам

        if state == State.HOLD:
            cmd.linear.x = 0.0
            cmd.angular.z = 0.0

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
