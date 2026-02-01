from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():

    return LaunchDescription([

        # IMU
        Node(
            package='tf2_ros',
            executable='static_transform_publisher',
            arguments=[
                '0', '0', '0',
                '0', '0', '0',
                'base_link',
                'imu_link'
            ]
        ),

        # Camera
        Node(
            package='tf2_ros',
            executable='static_transform_publisher',
            arguments=[
                '0.1', '0', '0',
                '0', '0', '0',
                'base_link',
                'camera_link'
            ]
        ),

        # LiDAR / Depth
        Node(
            package='tf2_ros',
            executable='static_transform_publisher',
            arguments=[
                '0.0', '0.0', '0.05',
                '0', '0', '0',
                'base_link',
                'lidar_link'
            ]
        ),
    ])
