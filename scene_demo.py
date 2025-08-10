#!/usr/bin/env python3
"""
Standalone scene demonstration script
Showcase RViz scenes based on MuJoCo assets
"""

import time
import logging
from main import ReachyController
from rviz_scene_manager import RVizSceneManager

logging.basicConfig(level=logging.INFO)

def demonstrate_all_scenes():
    """Demonstrate all available scenes"""
    print("🎬 Reachy2 Scene Demonstration")
    print("=" * 50)
    
    # Initialize controller
    controller = ReachyController(host="localhost")
    
    try:
        # Connect to robot
        print("Connecting to Reachy2...")
        if not controller.connect():
            print("❌ Failed to connect to Reachy2")
            return
        
        print("✅ Connected successfully!")
        
        # Initialize scene manager
        scene_manager = RVizSceneManager(controller.reachy)
        
        scenes_to_demo = [
            ("base_scene", "Empty base environment"),
            ("table_scene", "Simple table with red goal box"),
            ("fruits_scene", "Fruit sorting scenario with apples and oranges"),
            ("kitchen_scene", "Kitchen environment with tools and appliances")
        ]
        
        for scene_name, description in scenes_to_demo:
            print(f"\n🎭 Demonstrating: {scene_name}")
            print(f"Description: {description}")
            print("-" * 40)
            
            # Create scene
            if scene_name == "base_scene":
                success = scene_manager.create_base_scene()
            elif scene_name == "table_scene":
                success = scene_manager.create_table_scene()
            elif scene_name == "fruits_scene":
                success = scene_manager.create_fruits_scene()
            elif scene_name == "kitchen_scene":
                success = scene_manager.create_kitchen_scene()
            
            if success:
                print("✅ Scene created successfully!")
                
                # Demo object interaction for scenes with objects
                if scene_name in ["fruits_scene", "kitchen_scene"]:
                    print("🤖 Demonstrating object interaction...")
                    
                    # Get first object from scene
                    current_scene = scene_manager.get_current_scene()
                    if current_scene['objects']:
                        first_object = current_scene['objects'][0]['name']
                        scene_manager.simulate_object_interaction(first_object, "pick")
                
                # Pause between scenes
                input("\nPress Enter to continue to next scene...")
            else:
                print("❌ Failed to create scene")
        
        print("\n🎉 Scene demonstration completed!")
        print("Use 'python interactive_demo.py' for full interactive control")
        
    except Exception as e:
        print(f"❌ Error: {e}")
    finally:
        controller.disconnect()

if __name__ == "__main__":
    demonstrate_all_scenes()