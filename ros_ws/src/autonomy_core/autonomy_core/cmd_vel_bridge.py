#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
from rclpy.time import Time


class CmdVelBridge(Node):

    def __init__(self):
        super().__init__("cmd_vel_bridge")

        self.last_msg_time = self.get_clock().now()

        self.create_subscription(
            Twist,
            "/cmd_vel_autonomy",
            self.cb,
            10
        )

        self.pub = self.create_publisher(
            Twist,
            "/cmd_vel",
            10
        )

        self.timer = self.create_timer(0.1, self.watchdog)

        self.timeout = 0.5  # сек

        self.get_logger().info("CMD_VEL BRIDGE ONLINE")

    def cb(self, msg):
        self.last_msg_time = self.get_clock().now()
        self.pub.publish(msg)

    def watchdog(self):
        now = self.get_clock().now()

        if (now - self.last_msg_time).nanoseconds > self.timeout * 1e9:
            stop = Twist()
            self.pub.publish(stop)


def main():
    rclpy.init()
    node = CmdVelBridge()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()
