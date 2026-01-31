#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from rclpy.action import ActionClient

from nav2_msgs.action import NavigateToPose
from geometry_msgs.msg import PoseStamped


class MissionManager:

    def __init__(self, node: Node):
        self.node = node

        self.client = ActionClient(
            node,
            NavigateToPose,
            'navigate_to_pose'
        )

        self.active_goal = False

    def send_goal(self, x, y, yaw=0.0):

        if not self.client.wait_for_server(timeout_sec=2.0):
            self.node.get_logger().error("Nav2 action server not available")
            return

        goal = NavigateToPose.Goal()

        pose = PoseStamped()
        pose.header.frame_id = "map"
        pose.header.stamp = self.node.get_clock().now().to_msg()

        pose.pose.position.x = float(x)
        pose.pose.position.y = float(y)

        pose.pose.orientation.w = 1.0

        goal.pose = pose

        self.node.get_logger().info(
            f"MISSION → NAV2 GOAL: x={x} y={y}"
        )

        self.client.send_goal_async(goal)
        self.active_goal = True
