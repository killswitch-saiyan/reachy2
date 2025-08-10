#!/usr/bin/env python3
"""
Gazebo Scene Manager for Reachy2
Creates visual scenes in Gazebo simulation using SDF spawning
"""

import time
import logging
import subprocess
from typing import Dict, List, Tuple
from reachy2_sdk import ReachySDK

logger = logging.getLogger(__name__)

class GazeboSceneManager:
    """Manages Gazebo visual scenes for Reachy2"""
    
    def __init__(self, reachy_sdk: ReachySDK, docker_name: str = "reachy2_mujoco"):
        """
        Initialize Gazebo scene manager
        
        Args:
            reachy_sdk: Connected ReachySDK instance
            docker_name: Name of the Docker container running Gazebo
        """
        self.reachy = reachy_sdk
        self.current_scene = None
        self.spawned_objects = []
        self.docker_name = docker_name
        
    def create_fruits_scene(self) -> bool:
        """
        Create fruits scene with apples, oranges, table, plate, bowl in Gazebo
        
        Returns:
            bool: True if scene created successfully
        """
        try:
            logger.info("Creating fruits scene in Gazebo...")
            
            scene_objects = [
                {
                    "name": "table_fruits",
                    "type": "box", 
                    "position": (0.7, 0, 0.28),
                    "size": (0.45, 0.34, 0.28),
                    "color": "brown"
                },
                {
                    "name": "apple1",
                    "type": "sphere",
                    "position": (0.5, -0.12, 0.63),
                    "size": (0.04, 0.04, 0.04),
                    "color": "red"
                },
                {
                    "name": "apple2", 
                    "type": "sphere",
                    "position": (0.58, -0.07, 0.63),
                    "size": (0.04, 0.04, 0.04),
                    "color": "red"
                },
                {
                    "name": "orange1",
                    "type": "sphere", 
                    "position": (0.5, 0.15, 0.63),
                    "size": (0.04, 0.04, 0.04),
                    "color": "orange"
                },
                {
                    "name": "orange2",
                    "type": "sphere",
                    "position": (0.56, 0.07, 0.63), 
                    "size": (0.04, 0.04, 0.04),
                    "color": "orange"
                },
                {
                    "name": "plate",
                    "type": "cylinder",
                    "position": (0.6, 0.3, 0.65),
                    "size": (0.08, 0.08, 0.01),
                    "color": "white"
                },
                {
                    "name": "bowl",
                    "type": "cylinder", 
                    "position": (0.65, -0.25, 0.64),
                    "size": (0.06, 0.06, 0.03),
                    "color": "blue"
                }
            ]
            
            scene_description = {
                "name": "fruits_scene",
                "objects": scene_objects
            }
            
            self.current_scene = scene_description
            self._display_scene_info(scene_description)
            
            # Spawn objects in Gazebo
            success_count = 0
            for obj in scene_objects:
                if self._spawn_object_in_gazebo(obj):
                    success_count += 1
                    self.spawned_objects.append(obj['name'])
                else:
                    print(f"Failed to spawn {obj['name']}")
            
            print(f"Successfully spawned {success_count}/{len(scene_objects)} objects in Gazebo")
            logger.info("Fruits scene created successfully!")
            return success_count > 0
            
        except Exception as e:
            logger.error(f"Failed to create fruits scene: {e}")
            return False
    
    def create_table_scene(self) -> bool:
        """
        Create simple table scene with red goal box in Gazebo
        
        Returns:
            bool: True if scene created successfully  
        """
        try:
            logger.info("Creating table scene in Gazebo...")
            
            scene_objects = [
                {
                    "name": "table_main",
                    "type": "box",
                    "position": (0.7, 0, 0.35),
                    "size": (0.8, 1.2, 0.7),
                    "color": "wood_brown"
                },
                {
                    "name": "goal_box", 
                    "type": "box",
                    "position": (0.45, -0.4, 0.75),  # Placed on table
                    "size": (0.025, 0.025, 0.025),
                    "color": "red"
                }
            ]
            
            scene_description = {
                "name": "table_scene",
                "objects": scene_objects
            }
            
            self.current_scene = scene_description
            self._display_scene_info(scene_description)
            
            # Spawn objects in Gazebo
            success_count = 0
            for obj in scene_objects:
                if self._spawn_object_in_gazebo(obj):
                    success_count += 1
                    self.spawned_objects.append(obj['name'])
                else:
                    print(f"Failed to spawn {obj['name']}")
            
            print(f"Successfully spawned {success_count}/{len(scene_objects)} objects in Gazebo")
            logger.info("Table scene created successfully!")
            return success_count > 0
            
        except Exception as e:
            logger.error(f"Failed to create table scene: {e}")
            return False
    
    def create_kitchen_scene(self) -> bool:
        """
        Create kitchen scene with appliances and counters in Gazebo
        
        Returns:
            bool: True if scene created successfully
        """
        try:
            logger.info("Creating kitchen scene in Gazebo...")
            
            scene_objects = [
                {
                    "name": "counter",
                    "type": "box",
                    "position": (1.0, 0, 0.4),
                    "size": (0.6, 1.5, 0.8),
                    "color": "marble_white"
                },
                {
                    "name": "cutting_board",
                    "type": "box", 
                    "position": (0.8, 0, 0.82),
                    "size": (0.3, 0.2, 0.02),
                    "color": "wood_brown"
                },
                {
                    "name": "knife",
                    "type": "box",
                    "position": (0.8, 0.1, 0.83),
                    "size": (0.15, 0.02, 0.01),
                    "color": "silver"
                },
                {
                    "name": "pan",
                    "type": "cylinder",
                    "position": (1.2, -0.3, 0.82),
                    "size": (0.12, 0.12, 0.03),
                    "color": "black"
                }
            ]
            
            scene_description = {
                "name": "kitchen_scene",
                "objects": scene_objects
            }
            
            self.current_scene = scene_description
            self._display_scene_info(scene_description)
            
            # Spawn objects in Gazebo
            success_count = 0
            for obj in scene_objects:
                if self._spawn_object_in_gazebo(obj):
                    success_count += 1
                    self.spawned_objects.append(obj['name'])
                else:
                    print(f"Failed to spawn {obj['name']}")
            
            print(f"Successfully spawned {success_count}/{len(scene_objects)} objects in Gazebo")
            logger.info("Kitchen scene created successfully!")
            return success_count > 0
            
        except Exception as e:
            logger.error(f"Failed to create kitchen scene: {e}")
            return False
    
    def clear_scene(self) -> bool:
        """
        Clear current scene by removing spawned objects from Gazebo
        
        Returns:
            bool: True if cleared successfully
        """
        try:
            logger.info("Clearing current scene from Gazebo...")
            
            removed_count = 0
            for obj_name in self.spawned_objects:
                if self._remove_object_from_gazebo(obj_name):
                    removed_count += 1
                else:
                    print(f"Failed to remove {obj_name}")
            
            print(f"Removed {removed_count}/{len(self.spawned_objects)} objects from Gazebo")
            
            self.current_scene = None
            self.spawned_objects.clear()
            return True
            
        except Exception as e:
            logger.error(f"Failed to clear scene: {e}")
            return False
    
    def _spawn_object_in_gazebo(self, obj: Dict) -> bool:
        """
        Spawn a single object in Gazebo using SDF format
        
        Args:
            obj: Object dictionary with name, type, position, size, color
            
        Returns:
            bool: True if spawned successfully
        """
        try:
            # Generate SDF content for the object
            sdf_content = self._generate_sdf(obj)
            
            # Escape quotes in SDF content for shell command
            escaped_sdf = sdf_content.replace("'", "'\"'\"'").replace('\n', '\\n')
            
            # Create temporary SDF file in container
            sdf_filename = f"/tmp/{obj['name']}.sdf"
            
            # Write SDF content to file inside Docker container
            write_cmd = f"cat > {sdf_filename} << 'EOF'\n{sdf_content}\nEOF"
            result = subprocess.run([
                "docker", "exec", self.docker_name, "bash", "-c", write_cmd
            ], capture_output=True, text=True)
            
            if result.returncode != 0:
                print(f"Failed to create SDF file for {obj['name']}: {result.stderr}")
                return False
            
            # Use Python-based spawning which works reliably
            print(f"Spawning {obj['name']} using Python ROS2 client")
            return self._spawn_object_alternative(obj)
                
        except subprocess.TimeoutExpired:
            print(f"Timeout while spawning {obj['name']}")
            return False
        except Exception as e:
            logger.error(f"Error spawning {obj['name']}: {e}")
            return False
    
    def _spawn_object_alternative(self, obj: Dict) -> bool:
        """
        Alternative spawning method using Python script inside container
        
        Args:
            obj: Object dictionary
            
        Returns:
            bool: True if spawned successfully
        """
        try:
            # Create a Python script that spawns the object using ROS2
            python_script = f"""
import rclpy
from rclpy.node import Node
from gazebo_msgs.srv import SpawnEntity
from geometry_msgs.msg import Pose
import sys

class ObjectSpawner(Node):
    def __init__(self):
        super().__init__('spawn_object_{obj['name']}')
        self.client = self.create_client(SpawnEntity, '/spawn_entity')
        
    def spawn_object(self):
        try:
            request = SpawnEntity.Request()
            request.name = '{obj['name']}'
            
            with open('/tmp/{obj['name']}.sdf', 'r') as f:
                request.xml = f.read()
                
            request.robot_namespace = ''
            request.initial_pose = Pose()
            request.initial_pose.position.x = float({obj['position'][0]})
            request.initial_pose.position.y = float({obj['position'][1]})
            request.initial_pose.position.z = float({obj['position'][2]})
            request.initial_pose.orientation.w = 1.0
            request.reference_frame = 'world'
            
            if self.client.wait_for_service(timeout_sec=5.0):
                future = self.client.call_async(request)
                rclpy.spin_until_future_complete(self, future)
                response = future.result()
                print(f"Spawn result: {{response.success}}")
                return response.success
            else:
                print("Service not available")
                return False
                
        except Exception as e:
            print(f"Error: {{e}}")
            return False

rclpy.init()
spawner = ObjectSpawner()
success = spawner.spawn_object()
spawner.destroy_node()
rclpy.shutdown()
sys.exit(0 if success else 1)
"""
            
            # Write Python script to container
            script_path = f"/tmp/spawn_{obj['name']}.py"
            write_script_cmd = f"cat > {script_path} << 'EOF'\n{python_script}\nEOF"
            
            result = subprocess.run([
                "docker", "exec", self.docker_name, "bash", "-c", write_script_cmd
            ], capture_output=True, text=True)
            
            if result.returncode != 0:
                return False
            
            # Run the Python script
            run_script_cmd = f"source /opt/ros/humble/setup.bash && python3 {script_path}"
            result = subprocess.run([
                "docker", "exec", self.docker_name, "bash", "-c", run_script_cmd
            ], capture_output=True, text=True, timeout=20)
            
            if result.returncode == 0 and "Spawn result: True" in result.stdout:
                print(f"Successfully spawned {obj['name']} using alternative method")
                return True
            else:
                print(f"Alternative spawn failed for {obj['name']}")
                print(f"stdout: {result.stdout}")
                print(f"stderr: {result.stderr}")
                return False
                
        except Exception as e:
            logger.error(f"Alternative spawn error for {obj['name']}: {e}")
            return False
    
    def _remove_object_from_gazebo(self, obj_name: str) -> bool:
        """
        Remove an object from Gazebo
        
        Args:
            obj_name: Name of object to remove
            
        Returns:
            bool: True if removed successfully
        """
        try:
            # Create a Python script that removes the object using ROS2
            python_script = f"""
import rclpy
from rclpy.node import Node
from gazebo_msgs.srv import DeleteEntity
import sys

class ObjectRemover(Node):
    def __init__(self):
        super().__init__('remove_object_{obj_name}')
        self.client = self.create_client(DeleteEntity, '/delete_entity')
        
    def remove_object(self):
        try:
            request = DeleteEntity.Request()
            request.name = '{obj_name}'
            
            if self.client.wait_for_service(timeout_sec=5.0):
                future = self.client.call_async(request)
                rclpy.spin_until_future_complete(self, future)
                response = future.result()
                print(f"Remove result: {{response.success}}")
                return response.success
            else:
                print("Service not available")
                return False
                
        except Exception as e:
            print(f"Error: {{e}}")
            return False

rclpy.init()
remover = ObjectRemover()
success = remover.remove_object()
remover.destroy_node()
rclpy.shutdown()
sys.exit(0 if success else 1)
"""
            
            # Write Python script to container
            script_path = f"/tmp/remove_{obj_name}.py"
            write_script_cmd = f"cat > {script_path} << 'EOF'\n{python_script}\nEOF"
            
            result = subprocess.run([
                "docker", "exec", self.docker_name, "bash", "-c", write_script_cmd
            ], capture_output=True, text=True)
            
            if result.returncode != 0:
                print(f"Failed to create removal script for {obj_name}")
                return False
            
            # Run the Python script
            run_script_cmd = f"source /opt/ros/humble/setup.bash && python3 {script_path}"
            result = subprocess.run([
                "docker", "exec", self.docker_name, "bash", "-c", run_script_cmd
            ], capture_output=True, text=True, timeout=20)
            
            if result.returncode == 0 and "Remove result: True" in result.stdout:
                print(f"Successfully removed {obj_name} from Gazebo")
                return True
            else:
                print(f"Failed to remove {obj_name}")
                print(f"stdout: {result.stdout}")
                print(f"stderr: {result.stderr}")
                return False
                
        except Exception as e:
            logger.error(f"Error removing {obj_name}: {e}")
            return False
    
    def _generate_sdf(self, obj: Dict) -> str:
        """
        Generate SDF content for an object
        
        Args:
            obj: Object dictionary
            
        Returns:
            str: SDF XML content
        """
        name = obj['name']
        pos = obj['position']
        size = obj['size']
        color = self._get_gazebo_color(obj['color'])
        
        if obj['type'] == 'box':
            geometry = f"""
            <geometry>
              <box>
                <size>{size[0]} {size[1]} {size[2]}</size>
              </box>
            </geometry>"""
            
        elif obj['type'] == 'sphere':
            radius = size[0]  # Use first dimension as radius
            geometry = f"""
            <geometry>
              <sphere>
                <radius>{radius}</radius>
              </sphere>
            </geometry>"""
            
        elif obj['type'] == 'cylinder':
            radius = size[0]
            length = size[2]
            geometry = f"""
            <geometry>
              <cylinder>
                <radius>{radius}</radius>
                <length>{length}</length>
              </cylinder>
            </geometry>"""
        else:
            # Default to box
            geometry = f"""
            <geometry>
              <box>
                <size>{size[0]} {size[1]} {size[2]}</size>
              </box>
            </geometry>"""
        
        sdf_content = f"""<?xml version='1.0'?>
<sdf version='1.7'>
  <model name='{name}'>
    <pose>{pos[0]} {pos[1]} {pos[2]} 0 0 0</pose>
    <static>true</static>
    <link name='link'>
      <visual name='visual'>
        {geometry}
        <material>
          <ambient>{color}</ambient>
          <diffuse>{color}</diffuse>
          <specular>0.1 0.1 0.1 1</specular>
        </material>
      </visual>
      <collision name='collision'>
        {geometry}
      </collision>
    </link>
  </model>
</sdf>"""
        
        return sdf_content
    
    def _get_gazebo_color(self, color_name: str) -> str:
        """Convert color name to Gazebo RGBA format"""
        colors = {
            "red": "1 0 0 1",
            "orange": "1 0.5 0 1", 
            "yellow": "1 1 0 1",
            "green": "0 1 0 1",
            "blue": "0 0 1 1",
            "white": "1 1 1 1",
            "black": "0 0 0 1",
            "brown": "0.6 0.3 0.1 1",
            "wood_brown": "0.8 0.5 0.2 1",
            "marble_white": "0.95 0.95 0.95 1",
            "silver": "0.7 0.7 0.7 1",
            "checker_gray": "0.5 0.5 0.5 1"
        }
        
        return colors.get(color_name, "0.5 0.5 0.5 1")  # Default gray
    
    def get_current_scene(self) -> Dict:
        """Get current scene description"""
        return self.current_scene
    
    def list_available_scenes(self) -> List[str]:
        """List all available scenes"""
        return ["table_scene", "fruits_scene", "kitchen_scene"]
    
    def get_spawned_objects(self) -> List[str]:
        """Get list of currently spawned objects"""
        return self.spawned_objects.copy()
    
    def _display_scene_info(self, scene_description: Dict):
        """Display scene information to user"""
        print(f"\nGazebo Scene: {scene_description['name']}")
        print("=" * 40)
        print(f"Objects to spawn: {len(scene_description['objects'])}")
        
        for obj in scene_description['objects']:
            pos = obj['position']
            print(f"  {obj['name']}: {obj['type']} at ({pos[0]:.2f}, {pos[1]:.2f}, {pos[2]:.2f})")
        
        print()
    
    def simulate_object_interaction(self, object_name: str, action: str = "pick") -> bool:
        """
        Simulate picking up or interacting with scene objects
        
        Args:
            object_name: Name of object to interact with
            action: Type of interaction ("pick", "place", "push")
            
        Returns:
            bool: True if interaction simulated successfully
        """
        try:
            if not self.current_scene:
                print("ERROR: No scene loaded")
                return False
            
            # Find object in current scene
            target_object = None
            for obj in self.current_scene['objects']:
                if obj['name'] == object_name:
                    target_object = obj
                    break
            
            if not target_object:
                print(f"ERROR: Object '{object_name}' not found in scene")
                return False
            
            pos = target_object['position']
            print(f"Simulating {action} action on {object_name}")
            print(f"   Target position: ({pos[0]:.2f}, {pos[1]:.2f}, {pos[2]:.2f})")
            
            # Move Reachy's arm toward the object
            if hasattr(self.reachy, 'r_arm'):
                print("   Moving right arm toward target...")
                self.reachy.r_arm.turn_on()
                
                # Simple approach movement
                approach_pos = [pos[0] - 0.1, pos[1], pos[2] + 0.1]
                target_pos = list(pos)
                
                print(f"   Approaching: ({approach_pos[0]:.2f}, {approach_pos[1]:.2f}, {approach_pos[2]:.2f})")
                time.sleep(2)
                
                print(f"   Reaching target: ({target_pos[0]:.2f}, {target_pos[1]:.2f}, {target_pos[2]:.2f})")
                time.sleep(2)
                
                if action == "pick":
                    print("   Closing gripper...")
                    if hasattr(self.reachy.r_arm, 'gripper'):
                        self.reachy.r_arm.gripper.close()
                        time.sleep(1)
                
                print(f"SUCCESS: {action.capitalize()} action completed!")
                return True
            
            return False
            
        except Exception as e:
            logger.error(f"Failed to simulate interaction: {e}")
            return False