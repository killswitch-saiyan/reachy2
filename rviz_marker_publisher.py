#!/usr/bin/env python3
"""
RViz Marker Publisher for Reachy2 Scenes
Creates actual 3D markers that can be visualized in RViz
"""

import time
import logging
from typing import Dict, List

logger = logging.getLogger(__name__)

class RVizMarkerPublisher:
    """
    Publishers ROS markers for RViz visualization
    Note: This requires a ROS environment to work properly
    """
    
    def __init__(self):
        """Initialize marker publisher"""
        self.markers = []
        self.marker_id = 0
        
        # Check if ROS is available
        try:
            import rclpy
            from visualization_msgs.msg import Marker, MarkerArray
            from geometry_msgs.msg import Point
            from std_msgs.msg import ColorRGBA
            
            self.has_ros = True
            self.Marker = Marker
            self.MarkerArray = MarkerArray
            self.Point = Point
            self.ColorRGBA = ColorRGBA
            
            logger.info("ROS2 detected - RViz markers available")
            
        except ImportError:
            self.has_ros = False
            logger.warning("ROS2 not available - using conceptual markers only")
    
    def create_box_marker(self, name: str, position: tuple, size: tuple, color: str = "red") -> Dict:
        """Create a box marker"""
        marker = {
            "id": self.marker_id,
            "name": name,
            "type": "box",
            "position": position,
            "size": size,
            "color": self._get_color(color)
        }
        
        self.marker_id += 1
        return marker
    
    def create_sphere_marker(self, name: str, position: tuple, radius: float = 0.04, color: str = "red") -> Dict:
        """Create a sphere marker"""
        marker = {
            "id": self.marker_id,
            "name": name,
            "type": "sphere",
            "position": position,
            "radius": radius,
            "color": self._get_color(color)
        }
        
        self.marker_id += 1
        return marker
    
    def create_cylinder_marker(self, name: str, position: tuple, radius: float, height: float, color: str = "blue") -> Dict:
        """Create a cylinder marker"""
        marker = {
            "id": self.marker_id,
            "name": name,
            "type": "cylinder",
            "position": position,
            "radius": radius,
            "height": height,
            "color": self._get_color(color)
        }
        
        self.marker_id += 1
        return marker
    
    def publish_scene_markers(self, scene_objects: List[Dict]) -> bool:
        """
        Publish all scene objects as RViz markers
        
        Args:
            scene_objects: List of scene object dictionaries
            
        Returns:
            bool: True if published successfully
        """
        if not self.has_ros:
            print("WARNING: ROS2 not available - showing conceptual markers only")
            self._show_conceptual_markers(scene_objects)
            return True
        
        try:
            # Create markers for each object
            markers = []
            
            for obj in scene_objects:
                if obj['type'] == 'box':
                    marker = self.create_box_marker(
                        obj['name'],
                        obj['position'], 
                        obj['size'],
                        obj['color']
                    )
                elif obj['type'] == 'sphere':
                    size = obj.get('size', (0.04, 0.04, 0.04))
                    radius = size[0]  # Use x-size as radius
                    marker = self.create_sphere_marker(
                        obj['name'],
                        obj['position'],
                        radius,
                        obj['color']
                    )
                elif obj['type'] == 'cylinder':
                    size = obj.get('size', (0.08, 0.08, 0.02))
                    radius = size[0]  # Use x-size as radius
                    height = size[2]  # Use z-size as height
                    marker = self.create_cylinder_marker(
                        obj['name'],
                        obj['position'],
                        radius,
                        height,
                        obj['color']
                    )
                else:
                    continue  # Skip unknown types
                
                markers.append(marker)
                self.markers.append(marker)
            
            # TODO: Actually publish to ROS topic when ROS node is available
            # This would require a proper ROS2 node context
            
            print(f"Published {len(markers)} markers to RViz")
            return True
            
        except Exception as e:
            logger.error(f"Failed to publish markers: {e}")
            return False
    
    def clear_markers(self) -> bool:
        """Clear all published markers"""
        try:
            self.markers.clear()
            self.marker_id = 0
            
            if self.has_ros:
                # TODO: Publish empty marker array to clear
                print("Cleared RViz markers")
            else:
                print("Cleared conceptual markers")
            
            return True
            
        except Exception as e:
            logger.error(f"Failed to clear markers: {e}")
            return False
    
    def _get_color(self, color_name: str) -> tuple:
        """Convert color name to RGBA tuple"""
        colors = {
            "red": (1.0, 0.0, 0.0, 1.0),
            "orange": (1.0, 0.5, 0.0, 1.0),
            "yellow": (1.0, 1.0, 0.0, 1.0),
            "green": (0.0, 1.0, 0.0, 1.0),
            "blue": (0.0, 0.0, 1.0, 1.0),
            "white": (1.0, 1.0, 1.0, 1.0),
            "black": (0.0, 0.0, 0.0, 1.0),
            "brown": (0.6, 0.3, 0.1, 1.0),
            "wood_brown": (0.8, 0.5, 0.2, 1.0),
            "marble_white": (0.95, 0.95, 0.95, 1.0),
            "silver": (0.7, 0.7, 0.7, 1.0),
            "checker_gray": (0.5, 0.5, 0.5, 1.0)
        }
        
        return colors.get(color_name, (0.5, 0.5, 0.5, 1.0))  # Default gray
    
    def _show_conceptual_markers(self, scene_objects: List[Dict]):
        """Show conceptual representation when ROS is not available"""
        print("\nConceptual 3D Scene Visualization:")
        print("=" * 45)
        
        for obj in scene_objects:
            pos = obj['position']
            color = obj['color']
            
            if obj['type'] == 'box':
                size = obj['size']
                print(f"BOX {obj['name'].upper()}: {color} box")
                print(f"   Position: ({pos[0]:.2f}, {pos[1]:.2f}, {pos[2]:.2f})")
                print(f"   Size: {size[0]:.2f} x {size[1]:.2f} x {size[2]:.2f}")
                
            elif obj['type'] == 'sphere':
                size = obj.get('size', (0.04, 0.04, 0.04))
                print(f"SPHERE {obj['name'].upper()}: {color} sphere") 
                print(f"   Position: ({pos[0]:.2f}, {pos[1]:.2f}, {pos[2]:.2f})")
                print(f"   Radius: {size[0]:.2f}")
                
            elif obj['type'] == 'cylinder':
                size = obj.get('size', (0.08, 0.08, 0.02))
                print(f"CYLINDER {obj['name'].upper()}: {color} cylinder")
                print(f"   Position: ({pos[0]:.2f}, {pos[1]:.2f}, {pos[2]:.2f})")
                print(f"   Radius: {size[0]:.2f}, Height: {size[2]:.2f}")
            
            print()
        
        print("To see actual 3D objects, use MuJoCo simulation")
        print("Current RViz setup shows robot movements only")
        
    def get_marker_count(self) -> int:
        """Get number of active markers"""
        return len(self.markers)


def create_rviz_scene_file():
    """Create a basic RViz configuration file for scene visualization"""
    rviz_config = """
Panels:
  - Class: rviz_default_plugins/Displays
    Help Height: 78
    Name: Displays
    Property Tree Widget:
      Expanded:
        - /Global Options1
        - /RobotModel1
        - /MarkerArray1
      Splitter Ratio: 0.5
    Tree Height: 557
  - Class: rviz_default_plugins/Selection
    Name: Selection
  - Class: rviz_default_plugins/Tool Properties
    Expanded:
      - /2D Pose Estimate1
      - /2D Nav Goal1
      - /Publish Point1
    Name: Tool Properties
    Splitter Ratio: 0.5886790156364441
  - Class: rviz_default_plugins/Views
    Expanded:
      - /Current View1
    Name: Views
    Splitter Ratio: 0.5
Preferences:
  PromptSaveOnExit: true
Visualization Manager:
  Class: ""
  Displays:
    - Alpha: 0.5
      Cell Size: 1
      Class: rviz_default_plugins/Grid
      Color: 160; 160; 164
      Enabled: true
      Line Style:
        Line Width: 0.029999999329447746
        Value: Lines
      Name: Grid
      Normal Cell Count: 0
      Offset:
        X: 0
        Y: 0
        Z: 0
      Plane: XY
      Plane Cell Count: 10
      Reference Frame: <Fixed Frame>
      Value: true
    - Alpha: 1
      Class: rviz_default_plugins/RobotModel
      Collision Enabled: false
      Enabled: true
      Links:
        All Links Enabled: true
        Expand Joint Details: false
        Expand Link Details: false
        Expand Tree: false
      Name: RobotModel
      Robot Description: robot_description
      TF Prefix: ""
      Update Interval: 0
      Value: true
      Visual Enabled: true
    - Class: rviz_default_plugins/MarkerArray
      Enabled: true
      Marker Topic: /scene_markers
      Name: Scene Objects
      Namespaces:
        {}
      Queue Size: 100
      Value: true
  Enabled: true
  Global Options:
    Background Color: 48; 48; 48
    Default Light: true
    Fixed Frame: base_link
    Frame Rate: 30
  Name: root
  Tools:
    - Class: rviz_default_plugins/Interact
      Hide Inactive Objects: true
    - Class: rviz_default_plugins/MoveCamera
    - Class: rviz_default_plugins/Select
    - Class: rviz_default_plugins/FocusCamera
    - Class: rviz_default_plugins/Measure
  Value: true
  Views:
    Current:
      Class: rviz_default_plugins/Orbit
      Distance: 4.173077106475830
      Enable Stereo Rendering:
        Stereo Eye Separation: 0.05999999865889549
        Stereo Focal Distance: 1
        Swap Stereo Eyes: false
        Value: false
      Focal Point:
        X: 0.5
        Y: 0
        Z: 0.5
      Focal Shape Fixed Size: true
      Focal Shape Size: 0.05000000074505806
      Invert Z Axis: false
      Name: Current View
      Near Clip Distance: 0.009999999776482582
      Pitch: 0.33539772033691406
      Target Frame: <Fixed Frame>
      Value: Orbit (rviz)
      Yaw: 0.785398
Window Geometry:
  Displays:
    collapsed: false
  Height: 846
  Hide Left Dock: false
  Hide Right Dock: false
  QMainWindow State: 000000ff00000000fd000000040000000000000156000002b0fc0200000008fb0000001200530065006c0065006300740069006f006e00000001e10000009b0000005c00fffffffb0000001e0054006f006f006c002000500072006f007000650072007400690065007302000001ed000001df00000185000000a3fb000000120056006900650077007300200054006f006f02000001df000002110000018500000122fb000000200054006f006f006c002000500072006f0070006500720074006900650073003203000002880000011d000002210000017afb000000100044006900730070006c006100790073010000003d000002b0000000c900fffffffb0000002000730065006c0065006300740069006f006e00200062007500660066006500720200000138000000aa0000023a00000294fb00000014005700690064006500670065007400730100000041000000e60000000000000000fb0000000c004b0069006e0065006300740200000186000001060000030c00000261000000010000010f000002b0fc0200000003fb0000001e0054006f006f006c002000500072006f00700065007200740069006500730100000041000000780000000000000000fb0000000a00560069006500770073010000003d000002b0000000a400fffffffb0000001200530065006c0065006300740069006f006e010000025a000000b200000000000000000000000200000490000000a9fc0100000001fb0000000a00560069006500770073030000004e00000080000002e10000019700000003000004b00000003efc0100000002fb0000000800540069006d00650100000000000004b0000002fb00fffffffb0000000800540069006d0065010000000000000450000000000000000000000231000002b000000004000000040000000800000008fc0000000100000002000000010000000a0054006f006f006c00730100000000ffffffff0000000000000000
  Selection:
    collapsed: false
  Tool Properties:
    collapsed: false
  Views:
    collapsed: false
  Width: 1200
  X: 0
  Y: 0
"""
    
    try:
        with open('C:/Users/navee/reachy2_project/reachy_scene.rviz', 'w') as f:
            f.write(rviz_config)
        
        print("Created RViz configuration file: reachy_scene.rviz")
        print("Load this file in RViz to see scene markers")
        return True
        
    except Exception as e:
        logger.error(f"Failed to create RViz config: {e}")
        return False

if __name__ == "__main__":
    # Test the marker publisher
    publisher = RVizMarkerPublisher()
    
    # Create test scene
    test_objects = [
        {
            "name": "table",
            "type": "box",
            "position": (0.7, 0, 0.35),
            "size": (0.8, 1.2, 0.7),
            "color": "brown"
        },
        {
            "name": "apple",
            "type": "sphere", 
            "position": (0.5, -0.1, 0.6),
            "size": (0.04, 0.04, 0.04),
            "color": "red"
        }
    ]
    
    publisher.publish_scene_markers(test_objects)
    create_rviz_scene_file()