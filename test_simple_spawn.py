#!/usr/bin/env python3
"""
Simple test to spawn a single object in Gazebo
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from gazebo_scene_manager import GazeboSceneManager

def test_simple_spawn():
    """Test spawning a single simple object"""
    print("Testing Simple Object Spawning in Gazebo")
    print("=" * 45)
    
    # Create a mock ReachySDK for testing
    class MockReachySDK:
        def __init__(self):
            pass
    
    mock_reachy = MockReachySDK()
    scene_manager = GazeboSceneManager(mock_reachy, "reachy2_mujoco")
    
    # Test spawning a simple red box
    print("\nSpawning a simple red box...")
    
    simple_object = {
        "name": "test_red_box",
        "type": "box",
        "position": (0.5, 0.0, 1.0),  # 1m high so it's visible
        "size": (0.2, 0.2, 0.2),      # 20cm cube
        "color": "red"
    }
    
    if scene_manager._spawn_object_in_gazebo(simple_object):
        print("[SUCCESS] Red box spawned in Gazebo!")
        print("Check your Gazebo window - you should see a red cube!")
        
        # Wait and then remove it
        import time
        print("\nWaiting 5 seconds then removing object...")
        time.sleep(5)
        
        if scene_manager._remove_object_from_gazebo("test_red_box"):
            print("[SUCCESS] Object removed!")
        else:
            print("[WARNING] Failed to remove object")
    else:
        print("[FAILED] Failed to spawn red box")
    
    print("\nTest completed!")

if __name__ == "__main__":
    test_simple_spawn()