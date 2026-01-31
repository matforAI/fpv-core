from setuptools import setup

package_name = 'autonomy_core'

setup(
    name=package_name,
    version='0.0.1',
    packages=[package_name],
    data_files=[
        ('share/' + package_name + '/launch', ['launch/autonomy.launch.py']),
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='fpv',
    maintainer_email='dev@fpv.local',
    description='Autonomy core',
    license='MIT',
    entry_points={
        'console_scripts': [
            'autonomy_core = autonomy_core.core_node:main',
            'cmd_vel_bridge = autonomy_core.cmd_vel_bridge:main',
        ],
    },
)
