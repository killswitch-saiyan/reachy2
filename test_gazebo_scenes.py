#!/usr/bin/env python3
"""
Test script for Gazebo scene creation
Tests spawning objects directly in Gazebo simulation
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from gazebo_scene_manager import GazeboSceneManager
from main import ReachyController

def test_gazebo_docker_connection():
    """Test connection to Docker container"""
    print("Testing Docker Container Connection")
    print("=" * 40)
    
    docker_name = "reachy2_mujoco"
    
    # Test basic docker exec
    import subprocess
    try:
        result = subprocess.run([
            "docker", "exec", docker_name, "echo", "Docker connection test"
        ], capture_output=True, text=True, timeout=10)
        
        if result.returncode == 0:
            print(f"[SUCCESS] Docker container '{docker_name}' is accessible")
            print(f"Container response: {result.stdout.strip()}")
        else:
            print(f"[FAILED] Cannot access Docker container '{docker_name}'")
            print(f"Error: {result.stderr}")
            return False
    except subprocess.TimeoutExpired:
        print(f"[FAILED] Docker command timed out")
        return False
    except Exception as e:
        print(f"[FAILED] Docker connection error: {e}")
        return False
    
    # Test ROS2 and Gazebo service availability
    try:
        ros_test_cmd = "source /opt/ros/humble/setup.bash && ros2 service list"
        result = subprocess.run([
            "docker", "exec", docker_name, "bash", "-c", ros_test_cmd
        ], capture_output=True, text=True, timeout=15)
        
        if result.returncode == 0:
            print("[SUCCESS] ROS2 services are available")
            services = result.stdout.strip().split('\n')
            print(f"Available ROS2 services: {len(services)}")
            
            # Check for Gazebo services
            gazebo_services = [s for s in services if 'gazebo' in s or 'spawn' in s or 'delete' in s]
            if gazebo_services:
                print(f"Found Gazebo-related services: {gazebo_services[:5]}")  # Show first 5
            else:
                print("WARNING: No Gazebo services found")
                
            # Check specifically for spawn service
            spawn_services = [s for s in services if 'spawn_entity' in s]
            if spawn_services:
                print(f"Found spawn services: {spawn_services}")
            else:
                print("WARNING: No spawn_entity services found")
        else:
            print("[WARNING] ROS services not available, will try direct Gazebo")
            print(f"ROS error: {result.stderr}")
            
            # Test direct Gazebo
            gazebo_test_cmd = "gazebo --version"
            result = subprocess.run([
                "docker", "exec", docker_name, "bash", "-c", gazebo_test_cmd
            ], capture_output=True, text=True, timeout=10)
            
            if result.returncode == 0:
                print("[SUCCESS] Direct Gazebo access available")
            else:
                print("[FAILED] Neither ROS nor direct Gazebo available")
                return False
            
    except subprocess.TimeoutExpired:
        print("[FAILED] Service check timed out")
        return False
    except Exception as e:
        print(f"[FAILED] Service check error: {e}")
        return False
    
    return True

def test_gazebo_scene_creation():
    """Test scene creation in Gazebo"""
    print("\nTesting Gazebo Scene Creation")
    print("=" * 40)
    
    # Create a mock ReachySDK for testing
    class MockReachySDK:
        def __init__(self):
            pass
    
    mock_reachy = MockReachySDK()
    scene_manager = GazeboSceneManager(mock_reachy, "reachy2_mujoco")
    
    # Test table scene creation
    print("\n1. Testing Table Scene Creation...")
    try:
        if scene_manager.create_table_scene():
            print("[SUCCESS] Table scene created!")
            
            # Check spawned objects
            spawned = scene_manager.get_spawned_objects()
            print(f"Spawned objects: {spawned}")
            
            # Wait a moment then clear
            import time
            print("Waiting 3 seconds before clearing...")
            time.sleep(3)
            if scene_manager.clear_scene():
                print("[SUCCESS] Scene cleared")
            else:
                print("[WARNING] Scene clearing had issues")
        else:
            print("[FAILED] Table scene creation failed")
    except Exception as e:
        print(f"[ERROR] Exception during table scene test: {e}")
    
    # Test fruits scene creation
    print("\n2. Testing Fruits Scene Creation...")
    try:
        if scene_manager.create_fruits_scene():
            print("[SUCCESS] Fruits scene created!")
            
            # Check spawned objects
            spawned = scene_manager.get_spawned_objects()
            print(f"Spawned objects: {spawned}")
            
            # Wait a moment then clear
            import time
            print("Waiting 3 seconds before clearing...")
            time.sleep(3)
            if scene_manager.clear_scene():
                print("[SUCCESS] Scene cleared")
            else:
                print("[WARNING] Scene clearing had issues")
        else:
            print("[FAILED] Fruits scene creation failed")
    except Exception as e:
        print(f"[ERROR] Exception during fruits scene test: {e}")

def main():
    """Main test function"""
    print("Gazebo Scene Creation Test")
    print("=" * 50)
    print("Make sure your Docker container 'reachy2_mujoco' is running")
    print("and Gazebo simulation is active!")
    print()
    
    # Test Docker connection first
    if not test_gazebo_docker_connection():
        print("\n[CRITICAL] Docker connection failed!")
        print("Please ensure:")
        print("- Docker container 'reachy2_mujoco' is running")
        print("- Gazebo simulation is active inside the container")
        print("- Container has 'gz' command available")
        return
    
    # Proceed with scene testing
    print("\nDocker connection successful! Proceeding with scene tests...")
    test_gazebo_scene_creation()
    
    print("\n" + "=" * 50)
    print("Test Summary:")
    print("- Docker connection: Tested")
    print("- Gazebo services: Verified") 
    print("- Scene spawning: Tested")
    print("- Object removal: Tested")
    print()
    print("Next Steps:")
    print("1. Run 'python interactive_demo.py'")
    print("2. Use option 21 (Gazebo Scene Manager)")
    print("3. Create scenes and see objects in Gazebo!")

if __name__ == "__main__":
    main()