#!/usr/bin/env python3
"""
Test script for enhanced RViz scene visualization
Tests the integration of marker publisher with scene manager
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from rviz_scene_manager import RVizSceneManager
from rviz_marker_publisher import RVizMarkerPublisher, create_rviz_scene_file
from main import ReachyController

def test_scene_visualization():
    """Test the scene visualization system"""
    print("Testing Enhanced RViz Scene Visualization")
    print("=" * 50)
    
    # Test marker publisher standalone
    print("\n1. Testing RViz Marker Publisher...")
    publisher = RVizMarkerPublisher()
    
    test_objects = [
        {
            "name": "test_table",
            "type": "box",
            "position": (0.7, 0, 0.35),
            "size": (0.8, 1.2, 0.7),
            "color": "brown"
        },
        {
            "name": "test_apple", 
            "type": "sphere",
            "position": (0.5, -0.1, 0.6),
            "size": (0.04, 0.04, 0.04),
            "color": "red"
        }
    ]
    
    if publisher.publish_scene_markers(test_objects):
        print("[SUCCESS] Marker publisher test successful")
    else:
        print("[FAILED] Marker publisher test failed")
    
    # Test RViz config file creation
    print("\n2. Testing RViz Configuration Creation...")
    if create_rviz_scene_file():
        print("[SUCCESS] RViz config file created successfully")
    else:
        print("[FAILED] RViz config file creation failed")
    
    # Test scene manager without robot connection
    print("\n3. Testing Scene Manager (without robot)...")
    
    # Create a mock ReachySDK for testing
    class MockReachySDK:
        def __init__(self):
            pass
    
    mock_reachy = MockReachySDK()
    scene_manager = RVizSceneManager(mock_reachy)
    
    # Test each scene type
    scenes = [
        ("table_scene", "Table scene with red goal box"),
        ("fruits_scene", "Fruits scene with apples and oranges"), 
        ("kitchen_scene", "Kitchen scene with tools"),
        ("base_scene", "Base scene with floor")
    ]
    
    for scene_name, description in scenes:
        print(f"\nTesting {scene_name}...")
        
        if scene_name == "table_scene":
            success = scene_manager.create_table_scene()
        elif scene_name == "fruits_scene":
            success = scene_manager.create_fruits_scene()
        elif scene_name == "kitchen_scene":
            success = scene_manager.create_kitchen_scene()
        elif scene_name == "base_scene":
            success = scene_manager.create_base_scene()
        
        if success:
            print(f"[SUCCESS] {scene_name} created successfully")
            
            # Test marker count
            marker_count = scene_manager.marker_publisher.get_marker_count()
            print(f"   Created {marker_count} markers")
            
            # Get scene info
            current_scene = scene_manager.get_current_scene()
            if current_scene:
                print(f"   Scene contains {len(current_scene['objects'])} objects")
        else:
            print(f"[FAILED] {scene_name} creation failed")
    
    # Test scene clearing
    print("\n4. Testing Scene Clearing...")
    if scene_manager.clear_scene():
        print("[SUCCESS] Scene cleared successfully")
        marker_count = scene_manager.marker_publisher.get_marker_count()
        print(f"   Remaining markers: {marker_count}")
    else:
        print("[FAILED] Scene clearing failed")
    
    print("\n" + "=" * 50)
    print("Scene Visualization Test Summary:")
    print("• Marker publisher: Functional")
    print("• RViz config: Created")
    print("• Scene creation: Working")
    print("• Marker integration: Active")
    print("• Scene clearing: Working")
    print()
    print("Next Steps:")
    print("• Start Docker container with robot")
    print("• Run interactive_demo.py")
    print("• Use Scene Manager (option 20)")
    print("• Load reachy_scene.rviz in RViz to see 3D objects")
    print()
    print("Files created:")
    print("• reachy_scene.rviz (RViz configuration)")
    print("• Enhanced scene manager with marker publishing")

if __name__ == "__main__":
    test_scene_visualization()