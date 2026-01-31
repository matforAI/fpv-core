#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
from nav_msgs.msg import Odometry
from std_msgs.msg import String


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

        self.target_detected = False
        self.timer = self.create_timer(0.1, self.loop)

        self.get_logger().info("AUTONOMY CORE ONLINE")

    def on_detection(self, msg):
        self.target_detected = True

    def on_odom(self, msg):
        pass

    def loop(self):
        cmd = Twist()

        if self.target_detected:
            cmd.linear.x = 0.0
        else:
            cmd.linear.x = 0.3

        self.cmd_pub.publish(cmd)


def main():
    rclpy.init()
    node = AutonomyCore()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()
