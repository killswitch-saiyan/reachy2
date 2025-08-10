#!/usr/bin/env python3
"""
Interactive demo script for Reachy2 robot
Allows user to control robot through command-line interface
"""

import time
from main import ReachyController

def print_menu():
    """Print the interactive menu"""
    print("\n" + "="*50)
    print("REACHY2 INTERACTIVE CONTROL")
    print("="*50)
    print("1. Show robot status")
    print("2. Read joint positions")
    print("3. Move to neutral position")
    print("4. Wave hello (right arm)")
    print("5. Wave hello (left arm)")
    print("6. Move specific joint")
    print("7. Head movement demo")
    print("8. Quit")
    print("-"*50)

def demo_head_movement(controller):
    """Demonstrate head movements"""
    print("\nPerforming head movement demo...")
    
    movements = [
        ("neck.yaw", 0.5, 1.5, "Turn head right"),
        ("neck.yaw", -0.5, 1.5, "Turn head left"),
        ("neck.yaw", 0.0, 1.5, "Center head"),
        ("neck.pitch", -0.3, 1.5, "Look down"),
        ("neck.pitch", 0.3, 1.5, "Look up"),
        ("neck.pitch", 0.0, 1.5, "Center head"),
        ("neck.roll", 0.3, 1.0, "Tilt head right"),
        ("neck.roll", -0.3, 1.0, "Tilt head left"),
        ("neck.roll", 0.0, 1.0, "Center head"),
    ]
    
    for joint, position, duration, description in movements:
        print(f"  {description}...")
        controller.move_joint("head", joint, position, duration)
    
    print("[SUCCESS] Head movement demo completed")

def move_specific_joint(controller):
    """Allow user to move a specific joint"""
    print("\nAvailable parts: r_arm, l_arm, head")
    part = input("Enter part name: ").strip()
    
    if part not in ['r_arm', 'l_arm', 'head']:
        print("Invalid part name")
        return
    
    print(f"\nReading current joints for {part}...")
    positions = controller.read_joint_positions()
    
    if part in positions and isinstance(positions[part], dict):
        print(f"\nAvailable joints in {part}:")
        for joint_name, current_pos in positions[part].items():
            print(f"  {joint_name}: {current_pos:.3f} rad")
        
        joint = input("\nEnter joint name: ").strip()
        if joint not in positions[part]:
            print("Invalid joint name")
            return
        
        try:
            position = float(input(f"Enter target position in radians (current: {positions[part][joint]:.3f}): "))
            duration = float(input("Enter movement duration in seconds (default: 2.0): ") or "2.0")
            
            print(f"\nMoving {part}.{joint} to {position:.3f} rad...")
            success = controller.move_joint(part, joint, position, duration)
            
            if success:
                print("[SUCCESS] Movement completed")
            else:
                print("[FAILED] Movement failed")
                
        except ValueError:
            print("Invalid numeric input")
    else:
        print(f"Failed to read joints for {part}")

def main():
    """Main interactive demo"""
    print("Starting Reachy2 Interactive Demo...")
    
    # Initialize controller
    controller = ReachyController(host="localhost")
    
    try:
        # Connect to robot
        if not controller.connect():
            print("[ERROR] Failed to connect to Reachy2. Check if simulation is running at localhost:6080")
            return
        
        print("[SUCCESS] Connected to Reachy2 successfully!")
        
        while True:
            print_menu()
            
            try:
                choice = input("Enter your choice (1-8): ").strip()
                
                if choice == '1':
                    print("\n--- Robot Status ---")
                    info = controller.get_robot_info()
                    for key, value in info.items():
                        print(f"{key}: {value}")
                
                elif choice == '2':
                    print("\n--- Current Joint Positions ---")
                    positions = controller.read_joint_positions()
                    for part, joints in positions.items():
                        if isinstance(joints, dict):
                            print(f"\n{part.upper()}:")
                            for joint_name, position in joints.items():
                                print(f"  {joint_name}: {position:.3f} rad")
                
                elif choice == '3':
                    print("\nMoving to neutral position...")
                    if controller.move_to_neutral_position():
                        print("[SUCCESS] Robot moved to neutral position")
                    else:
                        print("[FAILED] Failed to move to neutral position")
                
                elif choice == '4':
                    print("\nPerforming wave gesture with right arm...")
                    if controller.wave_hello("r_arm"):
                        print("[SUCCESS] Wave gesture completed")
                    else:
                        print("[FAILED] Wave gesture failed")
                
                elif choice == '5':
                    print("\nPerforming wave gesture with left arm...")
                    if controller.wave_hello("l_arm"):
                        print("[SUCCESS] Wave gesture completed")
                    else:
                        print("[FAILED] Wave gesture failed")
                
                elif choice == '6':
                    move_specific_joint(controller)
                
                elif choice == '7':
                    demo_head_movement(controller)
                
                elif choice == '8':
                    print("\nExiting demo...")
                    break
                
                else:
                    print("Invalid choice. Please enter 1-8.")
                    
            except KeyboardInterrupt:
                print("\n\nExiting demo...")
                break
            except Exception as e:
                print(f"Error: {e}")
                
        print("\nDemo completed!")
        
    except Exception as e:
        print(f"❌ Demo error: {e}")
    finally:
        controller.disconnect()
        print("Disconnected from robot.")

if __name__ == "__main__":
    main()