import os

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource, FrontendLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration 

def generate_launch_description():
  worldName = LaunchConfiguration('worldName')
  vehicleHeight = LaunchConfiguration('vehicleHeight')
  cameraOffsetZ = LaunchConfiguration('cameraOffsetZ')
  vehicleX = LaunchConfiguration('vehicleX')
  vehicleY = LaunchConfiguration('vehicleY')
  vehicleZ = LaunchConfiguration('vehicleZ')
  terrainZ = LaunchConfiguration('terrainZ')
  vehicleYaw = LaunchConfiguration('vehicleYaw')
  gazeboTimeout = LaunchConfiguration('gazeboTimeout')
  checkTerrainConn = LaunchConfiguration('checkTerrainConn')
  gazebo_gui = LaunchConfiguration('gazebo_gui')
  
  declare_worldName = DeclareLaunchArgument('worldName', default_value="indoor", description='')
  declare_vehicleHeight = DeclareLaunchArgument('vehicleHeight', default_value='0.75', description='')
  declare_cameraOffsetZ = DeclareLaunchArgument('cameraOffsetZ', default_value='0.0', description='')
  declare_vehicleX = DeclareLaunchArgument('vehicleX', default_value='0.0', description='')
  declare_vehicleY = DeclareLaunchArgument('vehicleY', default_value='0.0', description='')
  declare_vehicleZ = DeclareLaunchArgument('vehicleZ', default_value='0.0', description='')
  declare_terrainZ = DeclareLaunchArgument('terrainZ', default_value='0.0', description='')
  declare_vehicleYaw = DeclareLaunchArgument('vehicleYaw', default_value='0.0', description='')
  declare_gazeboTimeout = DeclareLaunchArgument('gazeboTimeout', default_value='60.0', description='')
  declare_checkTerrainConn = DeclareLaunchArgument('checkTerrainConn', default_value='false', description='')
  declare_gazebo_gui = DeclareLaunchArgument('gazebo_gui', default_value='false', description='')

  start_gazebo = IncludeLaunchDescription(
    PythonLaunchDescriptionSource(os.path.join(
      get_package_share_directory('vehicle_simulator'), 'launch', 'gazebo.launch.py')
    ),
    launch_arguments={
      'worldName': worldName,
      'gui': gazebo_gui,
    }.items()
  )

  start_single_vehicle_system = IncludeLaunchDescription(
    PythonLaunchDescriptionSource(os.path.join(
      get_package_share_directory('vehicle_simulator'), 'launch', 'vehicle_with_planner.launch.py')
    ),
    launch_arguments={
      'robotName': 'robot_1',
      'vehicleHeight': vehicleHeight,
      'cameraOffsetZ': cameraOffsetZ,
      'vehicleX': vehicleX,
      'vehicleY': vehicleY,
      'vehicleZ': vehicleZ,
      'terrainZ': terrainZ,
      'vehicleYaw': vehicleYaw,
      'gazeboTimeout': gazeboTimeout,
      'checkTerrainConn': checkTerrainConn,
    }.items()
  )

  start_visualization = IncludeLaunchDescription(
    PythonLaunchDescriptionSource(os.path.join(
      get_package_share_directory('vehicle_simulator'), 'launch', 'visualization.launch.py')
    ),
    launch_arguments={
      'namespace': 'robot_1',
      'worldName': worldName,
    }.items()
  )

  ld = LaunchDescription()

  # Add the actions
  ld.add_action(declare_worldName)
  ld.add_action(declare_vehicleHeight)
  ld.add_action(declare_cameraOffsetZ)
  ld.add_action(declare_vehicleX)
  ld.add_action(declare_vehicleY)
  ld.add_action(declare_vehicleZ)
  ld.add_action(declare_terrainZ)
  ld.add_action(declare_vehicleYaw)
  ld.add_action(declare_gazeboTimeout)
  ld.add_action(declare_checkTerrainConn)
  ld.add_action(declare_gazebo_gui)

  ld.add_action(start_single_vehicle_system)
  ld.add_action(start_gazebo)
  ld.add_action(start_visualization)

  return ld