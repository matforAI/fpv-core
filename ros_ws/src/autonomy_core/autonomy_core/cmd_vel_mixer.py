#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
from std_msgs.msg import String
import json

class CmdVelMixer(Node):

    def __init__(self):
        super().__init__("cmd_vel_mixer")

        self.cmd_nav = Twist()
        self.cmd_auto = Twist()
        self.state = "NAV"

        self.create_subscription(
            Twist,
            "/cmd_vel_nav",
            self.on_nav,
            10
        )

        self.create_subscription(
            Twist,
            "/cmd_vel_autonomy",
            self.on_auto,
            10
        )

        self.create_subscription(
            String,
            "/swarm/status",
            self.on_state,
            10
        )

        self.pub = self.create_publisher(
            Twist,
            "/cmd_vel",
            10
        )

        self.timer = self.create_timer(0.05, self.tick)

        self.get_logger().info("CMD VEL MIXER READY")

    def on_nav(self, msg):
        self.cmd_nav = msg

    def on_auto(self, msg):
        self.cmd_auto = msg

    def on_state(self, msg):
        try:
            data = json.loads(msg.data)
            self.state = data.get("state", "NAV")
        except:
            pass

    def tick(self):
        cmd = Twist()

        if self.state in ["ANTI_COLLISION", "RTH", "TRACK"]:
            cmd = self.cmd_auto
        else:
            cmd = self.cmd_nav

        self.pub.publish(cmd)


def main():
    rclpy.init()
    node = CmdVelMixer()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == "__main__":
    main()
