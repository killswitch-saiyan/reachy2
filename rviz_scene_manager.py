#!/usr/bin/env python3
"""
RViz Scene Manager for Reachy2
Creates visual scenes inspired by MuJoCo assets repository
"""

import time
import logging
from typing import Dict, List, Tuple
from reachy2_sdk import ReachySDK
from rviz_marker_publisher import RVizMarkerPublisher

logger = logging.getLogger(__name__)

# Note: This is a conceptual implementation for demonstration
# RViz requires ROS nodes and marker publishers for actual 3D visualization
# The current implementation shows scene descriptions and simulates interactions

class RVizSceneManager:
    """Manages RViz visual scenes for Reachy2"""
    
    def __init__(self, reachy_sdk: ReachySDK):
        """
        Initialize scene manager
        
        Args:
            reachy_sdk: Connected ReachySDK instance
        """
        self.reachy = reachy_sdk
        self.current_scene = None
        self.marker_publisher = RVizMarkerPublisher()
        
    def create_fruits_scene(self) -> bool:
        """
        Create fruits scene with apples, oranges, table, plate, bowl
        Based on fruits_scene.xml from reachy2_mujoco_assets
        
        Returns:
            bool: True if scene created successfully
        """
        try:
            logger.info("Creating fruits scene...")
            
            # This is a conceptual implementation
            # RViz doesn't have built-in object spawning like MuJoCo
            # In practice, this would require ROS markers or URDF models
            
            scene_description = {
                "name": "fruits_scene",
                "objects": [
                    {
                        "name": "table",
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
            }
            
            self.current_scene = scene_description
            self._display_scene_info(scene_description)
            
            # Publish markers for visualization
            if self.marker_publisher.publish_scene_markers(scene_description['objects']):
                print("Scene markers published to RViz")
            else:
                print("Using conceptual visualization only")
            
            logger.info("✅ Fruits scene created successfully!")
            return True
            
        except Exception as e:
            logger.error(f"Failed to create fruits scene: {e}")
            return False
    
    def create_table_scene(self) -> bool:
        """
        Create simple table scene with red goal box
        Based on table_scene.xml from reachy2_mujoco_assets
        
        Returns:
            bool: True if scene created successfully  
        """
        try:
            logger.info("Creating table scene...")
            
            scene_description = {
                "name": "table_scene",
                "objects": [
                    {
                        "name": "table",
                        "type": "box",
                        "position": (0.7, 0, 0.35),
                        "size": (0.8, 1.2, 0.7),
                        "color": "wood_brown"
                    },
                    {
                        "name": "goal_box", 
                        "type": "box",
                        "position": (0.45, -0.4, 0.65),
                        "size": (0.025, 0.025, 0.025),
                        "color": "red"
                    }
                ]
            }
            
            self.current_scene = scene_description
            self._display_scene_info(scene_description)
            
            # Publish markers for visualization
            if self.marker_publisher.publish_scene_markers(scene_description['objects']):
                print("Scene markers published to RViz")
            else:
                print("Using conceptual visualization only")
            
            logger.info("✅ Table scene created successfully!")
            return True
            
        except Exception as e:
            logger.error(f"Failed to create table scene: {e}")
            return False
    
    def create_base_scene(self) -> bool:
        """
        Create empty base scene with just floor
        
        Returns:
            bool: True if scene created successfully
        """
        try:
            logger.info("Creating base scene...")
            
            scene_description = {
                "name": "base_scene",
                "objects": [
                    {
                        "name": "floor",
                        "type": "plane",
                        "position": (0, 0, 0),
                        "size": (10, 10, 0.1), 
                        "color": "checker_gray"
                    }
                ]
            }
            
            self.current_scene = scene_description
            self._display_scene_info(scene_description)
            
            # Publish markers for visualization
            if self.marker_publisher.publish_scene_markers(scene_description['objects']):
                print("Scene markers published to RViz")
            else:
                print("Using conceptual visualization only")
            
            logger.info("✅ Base scene created successfully!")
            return True
            
        except Exception as e:
            logger.error(f"Failed to create base scene: {e}")
            return False
    
    def create_kitchen_scene(self) -> bool:
        """
        Create kitchen scene with appliances and counters
        Conceptual kitchen environment
        
        Returns:
            bool: True if scene created successfully
        """
        try:
            logger.info("Creating kitchen scene...")
            
            scene_description = {
                "name": "kitchen_scene",
                "objects": [
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
            }
            
            self.current_scene = scene_description
            self._display_scene_info(scene_description)
            
            # Publish markers for visualization
            if self.marker_publisher.publish_scene_markers(scene_description['objects']):
                print("Scene markers published to RViz")
            else:
                print("Using conceptual visualization only")
            
            logger.info("✅ Kitchen scene created successfully!")
            return True
            
        except Exception as e:
            logger.error(f"Failed to create kitchen scene: {e}")
            return False
    
    def clear_scene(self) -> bool:
        """
        Clear current scene
        
        Returns:
            bool: True if cleared successfully
        """
        try:
            logger.info("Clearing current scene...")
            self.current_scene = None
            
            # Clear markers from RViz
            if self.marker_publisher.clear_markers():
                print("Scene and RViz markers cleared")
            else:
                print("Scene cleared (markers may still be visible)")
            
            return True
        except Exception as e:
            logger.error(f"Failed to clear scene: {e}")
            return False
    
    def get_current_scene(self) -> Dict:
        """Get current scene description"""
        return self.current_scene
    
    def list_available_scenes(self) -> List[str]:
        """List all available scenes"""
        return ["base_scene", "table_scene", "fruits_scene", "kitchen_scene"]
    
    def _display_scene_info(self, scene_description: Dict):
        """Display scene information to user"""
        print(f"\nScene: {scene_description['name']}")
        print("=" * 40)
        print(f"Objects in scene: {len(scene_description['objects'])}")
        
        for obj in scene_description['objects']:
            pos = obj['position']
            print(f"  {obj['name']}: {obj['type']} at ({pos[0]:.2f}, {pos[1]:.2f}, {pos[2]:.2f})")
        
        print()
    
    def _explain_rviz_visualization(self):
        """Explain RViz visualization capabilities"""
        print("RViz Visualization:")
        if self.marker_publisher.has_ros:
            print("   ROS2 detected - 3D markers will be published")
            print("   To see objects in RViz:")
            print("   • Load the reachy_scene.rviz configuration file")
            print("   • Subscribe to /scene_markers topic")
            print("   • Ensure ROS2 node is running for marker publishing")
        else:
            print("   ROS2 not available - using conceptual visualization")
            print("   What you CAN see:")
            print("   • Robot movements and interactions")
            print("   • Object positions and descriptions")
            print("   • Simulated picking/pointing actions")
        print()
        print("For physics simulation, use MuJoCo mode")
    
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
            
            # Move Reachy's arm toward the object (conceptual)
            if hasattr(self.reachy, 'r_arm'):
                print("   Moving right arm toward target...")
                self.reachy.r_arm.turn_on()
                
                # Simple approach movement
                approach_pos = [pos[0] - 0.1, pos[1], pos[2] + 0.1]
                target_pos = list(pos)
                
                print(f"   Approaching: ({approach_pos[0]:.2f}, {approach_pos[1]:.2f}, {approach_pos[2]:.2f})")
                # Note: In real implementation, would use inverse kinematics
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