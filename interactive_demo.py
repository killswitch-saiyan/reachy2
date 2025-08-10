#!/usr/bin/env python3
"""
Interactive demo script for Reachy2 robot
Allows user to control robot through command-line interface
"""

import time
import numpy as np
from main import ReachyController
from pyquaternion import Quaternion
from reachy2_sdk.utils.utils import get_pose_matrix

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
    print("8. Head look_at demo")
    print("9. Head goto demo (joint space)")
    print("10. Head rotate_by demo")
    print("11. Antenna control")
    print("12. Read head position")
    print("13. Gripper control (open/close)")
    print("14. Arm cartesian movement demo")
    print("15. Arm kinematics demo")
    print("16. Audio recording and playback")
    print("17. Audio file management")
    print("18. Quit")
    print("-"*50)

def demo_head_movement(controller):
    """Demonstrate head movements"""
    print("\nPerforming head movement demo...")
    print("Turning on head...")
    controller.reachy.head.turn_on()
    
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

def demo_head_look_at(controller):
    """Demonstrate head look_at functionality"""
    print("\nPerforming head look_at demo...")
    print("Turning on head...")
    controller.reachy.head.turn_on()
    
    movements = [
        (0.5, 0, 0.2, "Look forward"),
        (0.5, -0.3, 0.1, "Look right"),
        (0.5, 0, -0.4, "Look down"),
        (0.5, 0.3, -0.1, "Look left"),
        (0.5, 0, 0, "Look front center"),
    ]
    
    for x, y, z, description in movements:
        print(f"  {description}...")
        controller.reachy.head.look_at(x=x, y=y, z=z, duration=1.0, wait=True)
        time.sleep(0.5)
    
    print("[SUCCESS] Head look_at demo completed")

def demo_head_goto_joint(controller):
    """Demonstrate head goto in joint space"""
    print("\nPerforming head goto (joint space) demo...")
    print("Turning on head...")
    controller.reachy.head.turn_on()
    
    positions = [
        ([15, -20, 0], "Tilt right and down"),
        ([-15, 20, 0], "Tilt left and up"),
        ([0, 0, 30], "Turn right"),
        ([0, 0, -30], "Turn left"),
        ([0, 0, 0], "Return to center"),
    ]
    
    for pos, description in positions:
        print(f"  {description}...")
        controller.reachy.head.goto(pos, duration=1.0)
        time.sleep(1.5)
    
    print("[SUCCESS] Head goto demo completed")

def demo_head_rotate_by(controller):
    """Demonstrate head rotate_by functionality"""
    print("\nPerforming head rotate_by demo...")
    print("Turning on head...")
    controller.reachy.head.turn_on()
    
    rotations = [
        (0, 0, 20, 'head', "Rotate yaw right in head frame"),
        (0, 0, -40, 'head', "Rotate yaw left in head frame"),
        (-30, 0, 0, 'robot', "Rotate roll left in robot frame"),
        (60, 0, 0, 'robot', "Rotate roll right in robot frame"),
        (-30, 0, 20, 'robot', "Return to center"),
    ]
    
    for roll, pitch, yaw, frame, description in rotations:
        print(f"  {description}...")
        controller.reachy.head.rotate_by(roll=roll, pitch=pitch, yaw=yaw, frame=frame)
        time.sleep(1.5)
    
    print("[SUCCESS] Head rotate_by demo completed")

def demo_antenna_control(controller):
    """Demonstrate antenna control"""
    print("\nPerforming antenna control demo...")
    print("Turning on head (for antennas)...")
    controller.reachy.head.turn_on()
    
    movements = [
        (20, -20, "Antennas up and spread"),
        (0, 0, "Antennas center"),
        (-10, 10, "Antennas crossed"),
        (0, 0, "Return to center"),
    ]
    
    for r_pos, l_pos, description in movements:
        print(f"  {description}...")
        controller.reachy.head.r_antenna.goto(r_pos, duration=0.5)
        controller.reachy.head.l_antenna.goto(l_pos, duration=0.5)
        time.sleep(1.0)
    
    print("[SUCCESS] Antenna control demo completed")

def read_head_position(controller):
    """Read and display head position"""
    print("\n--- Head Position Information ---")
    
    # Cartesian space (quaternion)
    print("\nCartesian space (quaternion):")
    q = controller.reachy.head.get_current_orientation()
    print(f"Quaternion: {q}")
    
    # Joint space (roll, pitch, yaw)
    print("\nJoint space (degrees):")
    positions = controller.reachy.head.get_current_positions()
    print(f"Roll, Pitch, Yaw: {positions}")
    
    # Individual joint positions
    print("\nIndividual joint positions:")
    print(f"neck.roll: {controller.reachy.head.neck.roll.present_position:.3f} rad")
    print(f"neck.pitch: {controller.reachy.head.neck.pitch.present_position:.3f} rad")
    print(f"neck.yaw: {controller.reachy.head.neck.yaw.present_position:.3f} rad")
    print(f"l_antenna: {controller.reachy.head.l_antenna.present_position:.3f} rad")
    print(f"r_antenna: {controller.reachy.head.r_antenna.present_position:.3f} rad")

def demo_gripper_control(controller):
    """Demonstrate gripper control"""
    print("\nGripper Control Demo")
    print("Available arms: r_arm, l_arm")
    arm_choice = input("Choose arm (r_arm/l_arm): ").strip()
    
    if arm_choice not in ['r_arm', 'l_arm']:
        print("Invalid arm choice")
        return
    
    print(f"Turning on {arm_choice}...")
    if arm_choice == 'r_arm':
        controller.reachy.r_arm.turn_on()
        gripper = controller.reachy.r_arm.gripper
    else:
        controller.reachy.l_arm.turn_on()
        gripper = controller.reachy.l_arm.gripper
    
    print(f"\nCurrent gripper opening: {gripper.get_current_opening():.1f}%")
    
    actions = [
        ("close", "Closing gripper completely"),
        ("open", "Opening gripper completely"),
        ("set_50", "Setting gripper to 50% open"),
        ("set_75", "Setting gripper to 75% open"),
    ]
    
    for action, description in actions:
        print(f"  {description}...")
        
        if action == "close":
            gripper.close()
        elif action == "open": 
            gripper.open()
        elif action == "set_50":
            gripper.set_opening(50)
        elif action == "set_75":
            gripper.set_opening(75)
        
        # Wait for movement to complete
        while gripper.is_moving():
            time.sleep(0.1)
        
        print(f"    Current opening: {gripper.get_current_opening():.1f}%")
        time.sleep(1)
    
    print("[SUCCESS] Gripper control demo completed")

def demo_arm_cartesian(controller):
    """Demonstrate arm cartesian space movement"""
    print("\nArm Cartesian Movement Demo")
    print("Available arms: r_arm, l_arm")
    arm_choice = input("Choose arm (r_arm/l_arm): ").strip()
    
    if arm_choice not in ['r_arm', 'l_arm']:
        print("Invalid arm choice")
        return
    
    print(f"Turning on {arm_choice}...")
    if arm_choice == 'r_arm':
        controller.reachy.r_arm.turn_on()
        arm = controller.reachy.r_arm
    else:
        controller.reachy.l_arm.turn_on()
        arm = controller.reachy.l_arm
    
    print("Moving to elbow_90 posture...")
    arm.goto_posture('elbow_90', wait=True)
    
    # Get current pose
    current_pose = arm.forward_kinematics()
    print(f"Current gripper position: {current_pose[:3, 3]}")
    
    movements = [
        (0.1, 0, 0, "Move 10cm forward"),
        (0, 0.1, 0, "Move 10cm right"),
        (0, 0, 0.1, "Move 10cm up"),
        (-0.1, -0.1, -0.1, "Return to starting position"),
    ]
    
    for dx, dy, dz, description in movements:
        print(f"  {description}...")
        new_pose = current_pose.copy()
        new_pose[0, 3] += dx
        new_pose[1, 3] += dy  
        new_pose[2, 3] += dz
        
        arm.goto(new_pose, interpolation_space="cartesian_space", wait=True)
        time.sleep(0.5)
    
    print("Returning to default posture...")
    arm.goto_posture('default', wait=True)
    print("[SUCCESS] Cartesian movement demo completed")

def demo_arm_kinematics(controller):
    """Demonstrate forward and inverse kinematics"""
    print("\nArm Kinematics Demo")
    print("Available arms: r_arm, l_arm")
    arm_choice = input("Choose arm (r_arm/l_arm): ").strip()
    
    if arm_choice not in ['r_arm', 'l_arm']:
        print("Invalid arm choice")
        return
    
    print(f"Turning on {arm_choice}...")
    if arm_choice == 'r_arm':
        controller.reachy.r_arm.turn_on()
        arm = controller.reachy.r_arm
    else:
        controller.reachy.l_arm.turn_on()
        arm = controller.reachy.l_arm
    
    print("\n--- Forward Kinematics ---")
    joint_positions = [0, 10, -15, -90, 0, 0, -5]
    print(f"Joint positions: {joint_positions}")
    
    # Move to position
    arm.goto(joint_positions, wait=True)
    
    # Calculate forward kinematics
    pose = arm.forward_kinematics()
    position = pose[:3, 3]
    print(f"Forward kinematics result - Position: [{position[0]:.3f}, {position[1]:.3f}, {position[2]:.3f}]")
    
    print("\n--- Inverse Kinematics ---")
    # Create a target pose
    target_pose = get_pose_matrix([0.3, 0.1, -0.3], [0, -90, 0])
    print(f"Target position: [{target_pose[0,3]:.3f}, {target_pose[1,3]:.3f}, {target_pose[2,3]:.3f}]")
    
    # Calculate inverse kinematics
    ik_joints = arm.inverse_kinematics(target_pose)
    print(f"Inverse kinematics result - Joints: {[round(j, 1) for j in ik_joints]}")
    
    # Move to computed position
    print("Moving to computed joint positions...")
    arm.goto(ik_joints, wait=True)
    
    # Verify by calculating forward kinematics again
    verify_pose = arm.forward_kinematics()
    verify_position = verify_pose[:3, 3]
    print(f"Verification - Actual position: [{verify_position[0]:.3f}, {verify_position[1]:.3f}, {verify_position[2]:.3f}]")
    
    print("Returning to default posture...")
    arm.goto_posture('default', wait=True)
    print("[SUCCESS] Kinematics demo completed")

def demo_audio_recording(controller):
    """Demonstrate voice recording and playback"""
    print("\nAudio Recording and Playback Demo")
    print("This will record your voice and play it back!")
    
    # Show available audio files first
    print("\n--- Current Audio Files ---")
    try:
        files = controller.reachy.audio.get_audio_files()
        if files:
            for i, file in enumerate(files, 1):
                print(f"{i}. {file}")
        else:
            print("No audio files found")
    except Exception as e:
        print(f"Error getting audio files: {e}")
        return
    
    print("\n--- Recording Your Voice ---")
    duration = input("Enter recording duration in seconds (default: 5): ").strip()
    try:
        duration = int(duration) if duration else 5
    except ValueError:
        duration = 5
    
    filename = input("Enter filename for recording (default: my_voice.ogg): ").strip()
    if not filename:
        filename = "my_voice.ogg"
    if not filename.endswith('.ogg'):
        filename += '.ogg'
    
    print(f"Recording '{filename}' for {duration} seconds...")
    print("Start speaking now!")
    
    try:
        controller.reachy.audio.record_audio(filename, duration_secs=duration)
        
        # Wait for recording to complete
        import time
        time.sleep(duration + 1)  # Wait a bit extra to ensure recording is complete
        
        print(f"[SUCCESS] Recording completed: {filename}")
        
        # Check if file actually exists
        try:
            files = controller.reachy.audio.get_audio_files()
            if filename in files:
                print(f"✓ File '{filename}' confirmed in robot's storage")
            else:
                print(f"✗ File '{filename}' NOT found in robot's storage")
                print(f"Available files: {files}")
                return
        except Exception as e:
            print(f"Error checking files: {e}")
            return
        
        # Ask if user wants to play it back
        play_back = input("Do you want to play back the recording? (y/n): ").strip().lower()
        
        if play_back in ['y', 'yes']:
            print("Playing back your recording...")
            controller.reachy.audio.play_audio_file(filename)
            
            # Wait and ask if they want to stop
            time.sleep(2)
            stop = input("Press Enter to stop playback or wait for it to finish...")
            controller.reachy.audio.stop_playing()
            print("Playback stopped")
        
        # Ask if they want to download the file
        download = input("Do you want to download the file? (y/n): ").strip().lower()
        if download in ['y', 'yes']:
            download_path = input("Enter download path (default: C:/): ").strip()
            if not download_path:
                download_path = "C:/"
            
            try:
                controller.reachy.audio.download_audio_file(filename, download_path)
                print(f"[SUCCESS] File downloaded to {download_path}")
            except Exception as e:
                print(f"Download failed: {e}")
        
    except Exception as e:
        print(f"Recording failed: {e}")

def demo_audio_management(controller):
    """Demonstrate audio file management"""
    print("\nAudio File Management")
    
    while True:
        print("\n--- Audio Management Menu ---")
        print("1. List audio files")
        print("2. Upload audio file")
        print("3. Play audio file")
        print("4. Stop playback")
        print("5. Remove audio file")
        print("6. Download audio file")
        print("7. Back to main menu")
        
        choice = input("Enter your choice (1-7): ").strip()
        
        try:
            if choice == '1':
                print("\n--- Available Audio Files ---")
                files = controller.reachy.audio.get_audio_files()
                if files:
                    for i, file in enumerate(files, 1):
                        print(f"{i}. {file}")
                else:
                    print("No audio files found")
            
            elif choice == '2':
                file_path = input("Enter full path to audio file: ").strip()
                controller.reachy.audio.upload_audio_file(file_path)
                print("[SUCCESS] File uploaded successfully")
            
            elif choice == '3':
                files = controller.reachy.audio.get_audio_files()
                if not files:
                    print("No audio files available")
                    continue
                
                print("Available files:")
                for i, file in enumerate(files, 1):
                    print(f"{i}. {file}")
                
                file_choice = input("Enter filename to play: ").strip()
                controller.reachy.audio.play_audio_file(file_choice)
                print(f"Playing {file_choice}...")
            
            elif choice == '4':
                controller.reachy.audio.stop_playing()
                print("Playback stopped")
            
            elif choice == '5':
                files = controller.reachy.audio.get_audio_files()
                if not files:
                    print("No audio files to remove")
                    continue
                
                print("Available files:")
                for i, file in enumerate(files, 1):
                    print(f"{i}. {file}")
                
                file_to_remove = input("Enter filename to remove: ").strip()
                confirm = input(f"Are you sure you want to remove '{file_to_remove}'? (y/n): ").strip().lower()
                
                if confirm in ['y', 'yes']:
                    controller.reachy.audio.remove_audio_file(file_to_remove)
                    print(f"[SUCCESS] Removed {file_to_remove}")
                else:
                    print("Removal cancelled")
            
            elif choice == '6':
                files = controller.reachy.audio.get_audio_files()
                if not files:
                    print("No audio files to download")
                    continue
                
                print("Available files:")
                for i, file in enumerate(files, 1):
                    print(f"{i}. {file}")
                
                file_to_download = input("Enter filename to download: ").strip()
                download_path = input("Enter download path (default: C:/): ").strip()
                if not download_path:
                    download_path = "C:/"
                
                controller.reachy.audio.download_audio_file(file_to_download, download_path)
                print(f"[SUCCESS] Downloaded {file_to_download} to {download_path}")
            
            elif choice == '7':
                break
            
            else:
                print("Invalid choice. Please enter 1-7.")
                
        except Exception as e:
            print(f"Error: {e}")

def move_specific_joint(controller):
    """Allow user to move a specific joint"""
    print("\nAvailable parts: r_arm, l_arm, head")
    part = input("Enter part name: ").strip()
    
    if part not in ['r_arm', 'l_arm', 'head']:
        print("Invalid part name")
        return
    
    # Turn on the specific part
    print(f"Turning on {part}...")
    if part == 'r_arm':
        controller.reachy.r_arm.turn_on()
    elif part == 'l_arm':
        controller.reachy.l_arm.turn_on()
    elif part == 'head':
        controller.reachy.head.turn_on()
    
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
        
        # Turn on the robot so movements are visible
        print("Turning on robot...")
        controller.reachy.turn_on()
        print("[SUCCESS] Robot turned on!")
        
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
                    print("Turning on right arm...")
                    controller.reachy.r_arm.turn_on()
                    if controller.wave_hello("r_arm"):
                        print("[SUCCESS] Wave gesture completed")
                    else:
                        print("[FAILED] Wave gesture failed")
                
                elif choice == '5':
                    print("\nPerforming wave gesture with left arm...")
                    print("Turning on left arm...")
                    controller.reachy.l_arm.turn_on()
                    if controller.wave_hello("l_arm"):
                        print("[SUCCESS] Wave gesture completed")
                    else:
                        print("[FAILED] Wave gesture failed")
                
                elif choice == '6':
                    move_specific_joint(controller)
                
                elif choice == '7':
                    demo_head_movement(controller)
                
                elif choice == '8':
                    demo_head_look_at(controller)
                
                elif choice == '9':
                    demo_head_goto_joint(controller)
                
                elif choice == '10':
                    demo_head_rotate_by(controller)
                
                elif choice == '11':
                    demo_antenna_control(controller)
                
                elif choice == '12':
                    read_head_position(controller)
                
                elif choice == '13':
                    demo_gripper_control(controller)
                
                elif choice == '14':
                    demo_arm_cartesian(controller)
                
                elif choice == '15':
                    demo_arm_kinematics(controller)
                
                elif choice == '16':
                    demo_audio_recording(controller)
                
                elif choice == '17':
                    demo_audio_management(controller)
                
                elif choice == '18':
                    print("\nExiting demo...")
                    break
                
                else:
                    print("Invalid choice. Please enter 1-18.")
                    
            except KeyboardInterrupt:
                print("\n\nExiting demo...")
                break
            except Exception as e:
                print(f"Error: {e}")
                
        print("\nDemo completed!")
        
    except Exception as e:
        print(f"❌ Demo error: {e}")
    finally:
        # Turn off robot smoothly before disconnecting
        if controller.connected and controller.reachy:
            print("Turning off robot...")
            controller.reachy.turn_off_smoothly()
        controller.disconnect()
        print("Disconnected from robot.")

if __name__ == "__main__":
    main()