from launch import LaunchDescription
from launch_ros.actions import Node


def generate_launch_description():

    autonomy_core = Node(
        package='autonomy_core',
        executable='autonomy_core',
        name='autonomy_core',
        output='screen'
    )

    cmd_vel_bridge = Node(
        package='autonomy_core',
        executable='cmd_vel_bridge',
        name='cmd_vel_bridge',
        output='screen'
    )

    return LaunchDescription([
        autonomy_core,
        cmd_vel_bridge
    ])
