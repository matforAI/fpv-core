#!/usr/bin/env python3

import rclpy
from rclpy.node import Node

from geometry_msgs.msg import Twist
from nav_msgs.msg import Odometry
from std_msgs.msg import String

from autonomy_core.state_machine import StateMachine, State


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

        self.timer = self.create_timer(0.1, self.loop)

        self.get_logger().info("AUTONOMY CORE + STATE MACHINE STARTED")

    def on_detection(self, msg):
        self.has_detection = True

    def on_odom(self, msg):
        self.odom_ok = True

    def loop(self):

        state = self.sm.update(
            has_detection=self.has_detection,
            odom_ok=self.odom_ok
        )

        cmd = Twist()

        if state == State.IDLE:
            pass

        elif state == State.MOVE:
            cmd.linear.x = 0.4

        elif state == State.HOLD:
            cmd.linear.x = 0.0
            cmd.angular.z = 0.0

        elif state == State.FAIL:
            cmd.linear.x = 0.0
            cmd.angular.z = 0.0

        self.cmd_pub.publish(cmd)


def main():
    rclpy.init()
    node = AutonomyCore()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()
