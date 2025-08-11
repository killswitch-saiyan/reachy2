#!/usr/bin/env python3
"""
Reachy2 Mime Performance Script for MuJoCo
Based on the official Reachy tutorials - creates an invisible rope pulling performance
"""

import time
import logging
import numpy as np
from typing import List, Tuple
from reachy2_sdk import ReachySDK
from reachy2_sdk.utils.utils import get_pose_matrix

logger = logging.getLogger(__name__)

class MimePerformer:
    """Performs mime acts with Reachy2 robot"""
    
    def __init__(self, reachy_sdk: ReachySDK):
        """
        Initialize mime performer
        
        Args:
            reachy_sdk: Connected ReachySDK instance
        """
        self.reachy = reachy_sdk
        
    def perform_rope_pulling(self, duration: float = 30.0) -> bool:
        """
        Perform the classic mime rope pulling performance
        
        Args:
            duration: Total performance duration in seconds
            
        Returns:
            bool: True if performance completed successfully
        """
        try:
            print("🎭 Starting Mime Performance: Invisible Rope Pulling")
            print("=" * 50)
            
            # 1. Setup and preparation
            print("🎬 Act 1: Setting the stage...")
            if not self._setup_mime_position():
                return False
            
            time.sleep(2)
            
            # 2. Discovering the rope
            print("🎬 Act 2: Discovering the invisible rope...")
            if not self._discover_rope():
                return False
                
            time.sleep(1)
            
            # 3. Main rope pulling sequence
            print("🎬 Act 3: Pulling the rope...")
            start_time = time.time()
            pull_count = 0
            
            while time.time() - start_time < duration - 10:  # Save 10s for ending
                if not self._pull_rope_sequence(pull_count % 2 == 0):  # Alternate arms
                    break
                pull_count += 1
                time.sleep(0.5)  # Brief pause between pulls
            
            # 4. Finale - rope breaks
            print("🎬 Act 4: The rope breaks!")
            if not self._rope_breaks_finale():
                return False
            
            # 5. Bow
            print("🎬 Act 5: Taking a bow...")
            if not self._take_bow():
                return False
            
            print("🎭 Mime Performance Complete! 👏")
            return True
            
        except Exception as e:
            logger.error(f"Mime performance failed: {e}")
            print(f"❌ Performance interrupted: {e}")
            return False
        
        finally:
            # Ensure robot returns to safe position
            self._return_to_neutral()
    
    def _setup_mime_position(self) -> bool:
        """Set up initial mime position"""
        try:
            print("   🤖 Turning on robot systems...")
            
            # Turn on all parts
            self.reachy.turn_on()
            time.sleep(2)
            
            # Set head position - slightly turned left as if examining something
            print("   👤 Positioning head...")
            self.reachy.head.turn_on()
            self.reachy.head.goto([-10, 0, 0], duration=2.0)  # Slight left turn
            
            # Position arms in starting pose
            print("   🦾 Positioning arms...")
            self.reachy.r_arm.turn_on()
            self.reachy.l_arm.turn_on()
            
            # Arms at sides, elbows at 90 degrees
            self.reachy.r_arm.goto_posture('elbow_90', duration=3.0, wait=True)
            self.reachy.l_arm.goto_posture('elbow_90', duration=3.0, wait=True)
            
            # Open grippers
            print("   ✋ Opening hands...")
            self.reachy.r_arm.gripper.open()
            self.reachy.l_arm.gripper.open()
            
            return True
            
        except Exception as e:
            logger.error(f"Setup failed: {e}")
            return False
    
    def _discover_rope(self) -> bool:
        """Mime discovering the invisible rope"""
        try:
            # Head movement - looking for something
            print("   👀 Looking around curiously...")
            head_positions = [
                [-15, -10, 0],  # Look down left  
                [15, -10, 0],   # Look down right
                [0, 0, 0],      # Center
                [0, 10, 0],     # Look up
                [0, 0, 0]       # Back to center
            ]
            
            for pos in head_positions:
                self.reachy.head.goto(pos, duration=1.5, wait=True)
                time.sleep(0.5)
            
            # Right hand reaches out tentatively
            print("   🤚 Reaching out to feel for something...")
            r_current = self.reachy.r_arm.forward_kinematics()
            
            # Reach forward
            reach_pose = r_current.copy()
            reach_pose[0, 3] += 0.15  # Forward 15cm
            reach_pose[2, 3] += 0.1   # Up 10cm
            
            self.reachy.r_arm.goto(reach_pose, duration=2.0, 
                                 interpolation_space='cartesian_space', wait=True)
            
            # "Feel" the rope - small movements
            for _ in range(3):
                feel_pose = reach_pose.copy()
                feel_pose[1, 3] += 0.03  # Small side movement
                self.reachy.r_arm.goto(feel_pose, duration=0.5, 
                                     interpolation_space='cartesian_space', wait=True)
                
                feel_pose[1, 3] -= 0.06  # Back the other way
                self.reachy.r_arm.goto(feel_pose, duration=0.5,
                                     interpolation_space='cartesian_space', wait=True)
                
                feel_pose[1, 3] += 0.03  # Back to center
                self.reachy.r_arm.goto(feel_pose, duration=0.5,
                                     interpolation_space='cartesian_space', wait=True)
            
            # "Found it!" - close gripper
            print("   ✊ Found the rope!")
            self.reachy.r_arm.gripper.close()
            time.sleep(1)
            
            return True
            
        except Exception as e:
            logger.error(f"Rope discovery failed: {e}")
            return False
    
    def _pull_rope_sequence(self, use_right_arm: bool = True) -> bool:
        """
        Perform one rope pulling sequence
        
        Args:
            use_right_arm: If True, use right arm; if False, use left arm
        """
        try:
            arm = self.reachy.r_arm if use_right_arm else self.reachy.l_arm
            arm_name = "right" if use_right_arm else "left"
            
            print(f"   🪢 Pulling rope with {arm_name} arm...")
            
            # Get current position
            current_pose = arm.forward_kinematics()
            
            # Phase 1: Reach forward and grab
            reach_pose = current_pose.copy()
            reach_pose[0, 3] += 0.2   # Forward 20cm
            reach_pose[2, 3] += 0.05  # Slightly up
            
            # Move to reach position
            arm.goto(reach_pose, duration=1.0, 
                    interpolation_space='cartesian_space', wait=True)
            
            # Close gripper to "grab" rope
            arm.gripper.close()
            time.sleep(0.3)
            
            # Phase 2: Pull back with resistance
            pull_poses = []
            for i in range(5):  # 5 pull segments
                pull_pose = reach_pose.copy()
                pull_pose[0, 3] -= (i + 1) * 0.04  # Pull back 4cm each step
                pull_pose[2, 3] -= i * 0.01        # Slight downward curve
                pull_poses.append(pull_pose)
            
            # Execute pull with varying speed (showing resistance)
            for i, pose in enumerate(pull_poses):
                duration = 0.8 if i < 2 else 0.4  # Slower start, faster as rope "gives"
                arm.goto(pose, duration=duration,
                        interpolation_space='cartesian_space', wait=True)
                time.sleep(0.1)
            
            # Phase 3: Release and prepare for next pull
            arm.gripper.open()
            time.sleep(0.2)
            
            # Move back to starting position in an arc (avoid collision)
            intermediate_pose = current_pose.copy()
            intermediate_pose[2, 3] += 0.15  # Up 15cm
            arm.goto(intermediate_pose, duration=0.8,
                    interpolation_space='cartesian_space', wait=True)
            
            arm.goto(current_pose, duration=0.8,
                    interpolation_space='cartesian_space', wait=True)
            
            return True
            
        except Exception as e:
            logger.error(f"Rope pull sequence failed: {e}")
            return False
    
    def _rope_breaks_finale(self) -> bool:
        """Mime the rope breaking - dramatic finale"""
        try:
            # Both arms reach forward
            print("   🪢 Final pull - putting all strength into it...")
            
            r_current = self.reachy.r_arm.forward_kinematics()
            l_current = self.reachy.l_arm.forward_kinematics()
            
            # Both arms reach forward and grip
            r_reach = r_current.copy()
            r_reach[0, 3] += 0.25
            l_reach = l_current.copy() 
            l_reach[0, 3] += 0.25
            
            # Simultaneous reach
            self.reachy.r_arm.goto(r_reach, duration=1.5,
                                 interpolation_space='cartesian_space', wait=False)
            self.reachy.l_arm.goto(l_reach, duration=1.5,
                                 interpolation_space='cartesian_space', wait=True)
            
            # Both grippers close
            self.reachy.r_arm.gripper.close()
            self.reachy.l_arm.gripper.close()
            time.sleep(0.5)
            
            # Big pull back
            print("   💪 Pulling with maximum effort...")
            r_pull = r_reach.copy()
            r_pull[0, 3] -= 0.3
            r_pull[2, 3] -= 0.1
            
            l_pull = l_reach.copy()
            l_pull[0, 3] -= 0.3
            l_pull[2, 3] -= 0.1
            
            # Slow, strained pull
            self.reachy.r_arm.goto(r_pull, duration=3.0,
                                 interpolation_space='cartesian_space', wait=False)
            self.reachy.l_arm.goto(l_pull, duration=3.0,
                                 interpolation_space='cartesian_space', wait=True)
            
            time.sleep(0.5)
            
            # ROPE BREAKS! - sudden release
            print("   💥 SNAP! The rope breaks!")
            
            # Head reacts in surprise
            self.reachy.head.goto([0, -15, 0], duration=0.3, wait=False)  # Look down surprised
            
            # Arms fly back dramatically
            r_release = r_pull.copy()
            r_release[0, 3] -= 0.2  # Further back
            r_release[2, 3] += 0.15  # Up high
            
            l_release = l_pull.copy()
            l_release[0, 3] -= 0.2
            l_release[2, 3] += 0.15
            
            self.reachy.r_arm.goto(r_release, duration=0.5,
                                 interpolation_space='cartesian_space', wait=False)
            self.reachy.l_arm.goto(l_release, duration=0.5,
                                 interpolation_space='cartesian_space', wait=True)
            
            # Open grippers (rope is gone)
            self.reachy.r_arm.gripper.open()
            self.reachy.l_arm.gripper.open()
            
            # Look at hands in confusion
            print("   🤔 Where did the rope go?")
            time.sleep(1)
            
            # Head looks at each hand
            self.reachy.head.goto([20, 0, 15], duration=1.0, wait=True)  # Look at right hand
            time.sleep(1)
            self.reachy.head.goto([-20, 0, 15], duration=1.0, wait=True)  # Look at left hand
            time.sleep(1)
            self.reachy.head.goto([0, 0, 0], duration=1.0, wait=True)      # Center
            
            return True
            
        except Exception as e:
            logger.error(f"Rope break finale failed: {e}")
            return False
    
    def _take_bow(self) -> bool:
        """Take a bow at the end of performance"""
        try:
            print("   🙇 Taking a bow...")
            
            # Return arms to neutral first
            self.reachy.r_arm.goto_posture('default', duration=2.0, wait=False)
            self.reachy.l_arm.goto_posture('default', duration=2.0, wait=True)
            
            # Bow - head down
            self.reachy.head.goto([0, -30, 0], duration=2.0, wait=True)
            time.sleep(2)
            
            # Head back up
            self.reachy.head.goto([0, 0, 0], duration=2.0, wait=True)
            time.sleep(1)
            
            return True
            
        except Exception as e:
            logger.error(f"Bow failed: {e}")
            return False
    
    def _return_to_neutral(self):
        """Return robot to neutral position"""
        try:
            print("   🏠 Returning to neutral position...")
            self.reachy.goto_posture('default')
            
        except Exception as e:
            logger.error(f"Return to neutral failed: {e}")
    
    def perform_invisible_wall(self) -> bool:
        """
        Perform invisible wall mime act
        """
        try:
            print("🎭 Starting Mime Performance: Invisible Wall")
            print("=" * 50)
            
            # Setup
            self.reachy.turn_on()
            time.sleep(2)
            
            print("   🧱 Feeling the invisible wall...")
            
            # Both arms reach forward
            self.reachy.r_arm.turn_on()
            self.reachy.l_arm.turn_on()
            
            r_current = self.reachy.r_arm.forward_kinematics()
            l_current = self.reachy.l_arm.forward_kinematics()
            
            # Create wall positions
            wall_distance = 0.3  # 30cm in front
            wall_positions = [
                # Center
                (0, 0),
                # Move right
                (0.2, 0),
                # Move up
                (0.2, 0.2),
                # Move left
                (-0.2, 0.2),
                # Move down
                (-0.2, -0.2),
                # Back to center
                (0, 0)
            ]
            
            for y_offset, z_offset in wall_positions:
                # Right arm
                r_wall = r_current.copy()
                r_wall[0, 3] = r_current[0, 3] + wall_distance
                r_wall[1, 3] = r_current[1, 3] + y_offset
                r_wall[2, 3] = r_current[2, 3] + z_offset
                
                # Left arm 
                l_wall = l_current.copy()
                l_wall[0, 3] = l_current[0, 3] + wall_distance
                l_wall[1, 3] = l_current[1, 3] - y_offset  # Mirror
                l_wall[2, 3] = l_current[2, 3] + z_offset
                
                # Move both arms
                self.reachy.r_arm.goto(r_wall, duration=2.0,
                                     interpolation_space='cartesian_space', wait=False)
                self.reachy.l_arm.goto(l_wall, duration=2.0,
                                     interpolation_space='cartesian_space', wait=True)
                
                time.sleep(1)
            
            print("🎭 Invisible Wall Performance Complete!")
            return True
            
        except Exception as e:
            logger.error(f"Invisible wall performance failed: {e}")
            return False
        
        finally:
            self._return_to_neutral()

def demo_mime_performance(controller):
    """Demo function for mime performance"""
    print("\n🎭 Reachy2 Mime Performance")
    print("Choose your performance:")
    print("1. Invisible Rope Pulling (Classic)")
    print("2. Invisible Wall")
    print("3. Both performances")
    
    choice = input("Enter choice (1-3): ").strip()
    
    try:
        mime = MimePerformer(controller.reachy)
        
        if choice == '1':
            duration = input("Performance duration in seconds (default: 30): ").strip()
            duration = int(duration) if duration else 30
            
            print(f"\n🎬 Starting {duration}-second rope pulling performance...")
            print("Watch in MuJoCo simulation!")
            
            if mime.perform_rope_pulling(duration):
                print("🎉 Performance completed successfully!")
            else:
                print("❌ Performance failed")
                
        elif choice == '2':
            print("\n🎬 Starting invisible wall performance...")
            print("Watch in MuJoCo simulation!")
            
            if mime.perform_invisible_wall():
                print("🎉 Performance completed successfully!")
            else:
                print("❌ Performance failed")
                
        elif choice == '3':
            print("\n🎬 Starting full mime show...")
            print("First: Invisible Wall")
            
            if mime.perform_invisible_wall():
                print("✅ First act complete!")
                time.sleep(3)
                
                print("Second: Rope Pulling")
                if mime.perform_rope_pulling(25):
                    print("🎉 Full show completed successfully!")
                else:
                    print("❌ Second act failed")
            else:
                print("❌ First act failed")
        else:
            print("Invalid choice")
            
    except Exception as e:
        print(f"❌ Mime performance error: {e}")