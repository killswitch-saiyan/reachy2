#!/usr/bin/env python3
"""
Reachy2 Robot Control Application
Main entry point for controlling Reachy2 robot through SDK
"""

import time
import logging
import math
from typing import Optional, Dict, Tuple
from reachy2_sdk.reachy_sdk import ReachySDK

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Joint safety limits (in radians)
JOINT_LIMITS = {
    'r_arm': {
        'shoulder.pitch': (-math.pi, math.pi/2),
        'shoulder.roll': (-math.pi/2, math.pi/2),
        'elbow.yaw': (-math.pi, math.pi),
        'elbow.pitch': (-math.pi, 0),
        'wrist.roll': (-math.pi, math.pi),
        'wrist.pitch': (-math.pi/2, math.pi/2),
        'wrist.yaw': (-math.pi, math.pi),
        'gripper': (0, math.pi/2)
    },
    'l_arm': {
        'shoulder.pitch': (-math.pi, math.pi/2),
        'shoulder.roll': (-math.pi/2, math.pi/2),
        'elbow.yaw': (-math.pi, math.pi),
        'elbow.pitch': (0, math.pi),
        'wrist.roll': (-math.pi, math.pi),
        'wrist.pitch': (-math.pi/2, math.pi/2),
        'wrist.yaw': (-math.pi, math.pi),
        'gripper': (0, math.pi/2)
    },
    'head': {
        'neck.roll': (-math.pi/4, math.pi/4),
        'neck.pitch': (-math.pi/4, math.pi/4),
        'neck.yaw': (-math.pi/2, math.pi/2),
        'l_antenna': (0, math.pi/2),
        'r_antenna': (0, math.pi/2)
    }
}


class ReachyController:
    """Main controller class for Reachy2 robot operations"""
    
    def __init__(self, host: str = "localhost", port: int = 50055):
        """
        Initialize connection to Reachy2 robot
        
        Args:
            host: Robot IP address or hostname
            port: Connection port
        """
        self.host = host
        self.port = port
        self.reachy: Optional[ReachySDK] = None
        self.connected = False
    
    def connect(self) -> bool:
        """
        Establish connection to Reachy2 robot
        
        Returns:
            bool: True if connection successful
        """
        try:
            logger.info(f"Connecting to Reachy2 at {self.host}:{self.port}")
            self.reachy = ReachySDK(host=self.host)
            
            # Test connection with timeout
            import time
            logger.info("Testing connection...")
            time.sleep(2)
            
            # Try to get robot info to verify connection
            try:
                info = self.reachy.info
                logger.info(f"Robot info: {info}")
                self.connected = True
                logger.info("Successfully connected to Reachy2")
                return True
            except Exception as conn_test_error:
                logger.error(f"Connection test failed: {conn_test_error}")
                return False
        except Exception as e:
            logger.error(f"Failed to connect to Reachy2: {e}")
            self.connected = False
            return False
    
    def perform_intro_setup(self, speed: str = "medium") -> bool:
        """
        Perform intro setup sequence: head down -> turn on -> head up
        
        Args:
            speed: Animation speed ("slow", "medium", "fast")
            
        Returns:
            bool: True if intro successful
        """
        if not self.connected or not self.reachy:
            logger.error("Not connected to robot")
            return False
        
        try:
            logger.info("Starting Reachy2 intro setup sequence...")
            
            # Set movement durations based on speed
            duration_map = {
                "slow": 3.0,
                "medium": 2.0, 
                "fast": 1.0
            }
            move_duration = duration_map.get(speed, 2.0)
            
            # Step 1: Turn on head only (for initial positioning)
            logger.info("Turning on head for positioning...")
            self.reachy.head.turn_on()
            time.sleep(1)
            
            # Step 2: Move head to "down" position
            logger.info("Moving head to down position...")
            # Look down: forward and significantly down
            self.reachy.head.look_at(x=0.3, y=0, z=-0.4, duration=move_duration, wait=True)
            time.sleep(0.5)
            
            # Step 3: Turn on full robot
            logger.info("Turning on full robot...")
            self.reachy.turn_on()
            time.sleep(1)
            
            # Step 4: Graceful head movement to up/forward position
            logger.info("Moving head to greeting position...")
            # Look forward and slightly up for a welcoming pose
            self.reachy.head.look_at(x=0.5, y=0, z=0.1, duration=move_duration, wait=True)
            
            # Step 5: Optional antenna greeting
            logger.info("Adding personality with antenna movement...")
            # Subtle antenna movement for personality
            self.reachy.head.l_antenna.goto(10, duration=0.8)
            self.reachy.head.r_antenna.goto(-10, duration=0.8) 
            time.sleep(1)
            
            # Return antennas to neutral
            self.reachy.head.l_antenna.goto(0, duration=0.8)
            self.reachy.head.r_antenna.goto(0, duration=0.8)
            time.sleep(1)
            
            logger.info("✨ Intro setup sequence completed successfully!")
            print("\n🤖 Hello! Reachy2 is ready for action!")
            return True
            
        except Exception as e:
            logger.error(f"Intro setup failed: {e}")
            return False
    
    def reset_to_down_position(self) -> bool:
        """
        Reset robot to head-down starting position
        
        Returns:
            bool: True if reset successful
        """
        if not self.connected or not self.reachy:
            logger.error("Not connected to robot")
            return False
            
        try:
            logger.info("Resetting to head-down position...")
            
            # Turn on head if not already on
            if not self.reachy.head.is_on():
                self.reachy.head.turn_on()
                time.sleep(1)
            
            # Move to down position
            self.reachy.head.look_at(x=0.3, y=0, z=-0.4, duration=2.0, wait=True)
            
            # Turn off robot but keep head position
            self.reachy.turn_off_smoothly()
            
            logger.info("Reset to down position completed")
            return True
            
        except Exception as e:
            logger.error(f"Reset to down position failed: {e}")
            return False
    
    def disconnect(self):
        """Disconnect from Reachy2 robot"""
        if self.reachy and self.connected:
            self.reachy.disconnect()
            self.connected = False
            logger.info("Disconnected from Reachy2")
    
    def get_robot_info(self) -> dict:
        """
        Get basic robot information and status
        
        Returns:
            dict: Robot information
        """
        if not self.connected or not self.reachy:
            return {"error": "Not connected to robot"}
        
        try:
            info = {
                "connected": self.connected,
                "host": self.host,
                "available_parts": [],
                "joint_states": {}
            }
            
            # Get available parts
            if hasattr(self.reachy, 'r_arm'):
                info["available_parts"].append("right_arm")
            if hasattr(self.reachy, 'l_arm'):
                info["available_parts"].append("left_arm")
            if hasattr(self.reachy, 'head'):
                info["available_parts"].append("head")
            
            return info
            
        except Exception as e:
            logger.error(f"Error getting robot info: {e}")
            return {"error": str(e)}
    
    def read_joint_positions(self) -> dict:
        """
        Read current joint positions from all available parts
        
        Returns:
            dict: Joint positions by part
        """
        if not self.connected or not self.reachy:
            return {"error": "Not connected to robot"}
        
        try:
            positions = {}
            
            # Read right arm joints if available
            if hasattr(self.reachy, 'r_arm'):
                positions['right_arm'] = {}
                try:
                    # Get all joints from the right arm
                    for joint_name, joint in self.reachy.r_arm.joints.items():
                        positions['right_arm'][joint_name] = joint.present_position
                except Exception as e:
                    positions['right_arm'] = {"error": str(e)}
            
            # Read left arm joints if available
            if hasattr(self.reachy, 'l_arm'):
                positions['left_arm'] = {}
                try:
                    # Get all joints from the left arm
                    for joint_name, joint in self.reachy.l_arm.joints.items():
                        positions['left_arm'][joint_name] = joint.present_position
                except Exception as e:
                    positions['left_arm'] = {"error": str(e)}
            
            # Read head joints if available
            if hasattr(self.reachy, 'head'):
                positions['head'] = {}
                try:
                    # Get all joints from the head
                    for joint_name, joint in self.reachy.head.joints.items():
                        positions['head'][joint_name] = joint.present_position
                except Exception as e:
                    positions['head'] = {"error": str(e)}
            
            return positions
            
        except Exception as e:
            logger.error(f"Error reading joint positions: {e}")
            return {"error": str(e)}
    
    def validate_joint_position(self, part: str, joint_name: str, position: float) -> bool:
        """
        Validate that a joint position is within safety limits
        
        Args:
            part: Robot part name
            joint_name: Joint name
            position: Target position in radians
            
        Returns:
            bool: True if position is safe
        """
        if part not in JOINT_LIMITS:
            logger.warning(f"No safety limits defined for part '{part}'")
            return True
        
        if joint_name not in JOINT_LIMITS[part]:
            logger.warning(f"No safety limits defined for joint '{part}.{joint_name}'")
            return True
        
        min_pos, max_pos = JOINT_LIMITS[part][joint_name]
        
        if position < min_pos or position > max_pos:
            logger.error(f"Position {position:.3f} for {part}.{joint_name} exceeds safety limits [{min_pos:.3f}, {max_pos:.3f}]")
            return False
        
        return True
    
    def move_joint(self, part: str, joint_name: str, position: float, duration: float = 2.0) -> bool:
        """
        Move a specific joint to target position
        
        Args:
            part: Robot part ('r_arm', 'l_arm', 'head')
            joint_name: Name of the joint
            position: Target position in radians
            duration: Movement duration in seconds
            
        Returns:
            bool: True if movement successful
        """
        if not self.connected or not self.reachy:
            logger.error("Not connected to robot")
            return False
        
        try:
            # Validate safety limits
            if not self.validate_joint_position(part, joint_name, position):
                return False
            
            # Get the robot part
            robot_part = getattr(self.reachy, part, None)
            if robot_part is None:
                logger.error(f"Robot part '{part}' not available")
                return False
            
            # Get the joint
            if joint_name not in robot_part.joints:
                logger.error(f"Joint '{joint_name}' not found in {part}")
                return False
            
            joint = robot_part.joints[joint_name]
            
            # Set target position
            joint.goal_position = position
            logger.info(f"Moving {part}.{joint_name} to {position:.3f} rad over {duration}s")
            
            # Wait for movement to complete
            time.sleep(duration)
            
            return True
            
        except Exception as e:
            logger.error(f"Error moving joint {part}.{joint_name}: {e}")
            return False
    
    def move_to_neutral_position(self, duration: float = 3.0) -> bool:
        """
        Move robot to neutral/home position
        
        Args:
            duration: Movement duration in seconds
            
        Returns:
            bool: True if movement successful
        """
        if not self.connected or not self.reachy:
            logger.error("Not connected to robot")
            return False
        
        try:
            logger.info("Moving robot to neutral position")
            
            # Move arms to neutral position
            if hasattr(self.reachy, 'r_arm'):
                for joint_name, joint in self.reachy.r_arm.joints.items():
                    joint.goal_position = 0.0
            
            if hasattr(self.reachy, 'l_arm'):
                for joint_name, joint in self.reachy.l_arm.joints.items():
                    joint.goal_position = 0.0
            
            # Move head to neutral position
            if hasattr(self.reachy, 'head'):
                for joint_name, joint in self.reachy.head.joints.items():
                    joint.goal_position = 0.0
            
            # Wait for movement to complete
            time.sleep(duration)
            
            logger.info("Robot moved to neutral position")
            return True
            
        except Exception as e:
            logger.error(f"Error moving to neutral position: {e}")
            return False
    
    def wave_hello(self, arm: str = "r_arm") -> bool:
        """
        Perform a simple wave gesture
        
        Args:
            arm: Which arm to use ('r_arm' or 'l_arm')
            
        Returns:
            bool: True if gesture successful
        """
        if not self.connected or not self.reachy:
            logger.error("Not connected to robot")
            return False
        
        try:
            logger.info(f"Performing wave gesture with {arm}")
            
            # Get the arm
            robot_arm = getattr(self.reachy, arm, None)
            if robot_arm is None:
                logger.error(f"Arm '{arm}' not available")
                return False
            
            # Wave sequence
            movements = [
                ("shoulder.pitch", -0.5, 1.0),  # Raise arm
                ("elbow.pitch", -1.2, 1.0),    # Bend elbow
                ("wrist.yaw", 0.5, 0.5),       # Wave right
                ("wrist.yaw", -0.5, 0.5),      # Wave left
                ("wrist.yaw", 0.5, 0.5),       # Wave right
                ("wrist.yaw", 0.0, 0.5),       # Center wrist
                ("elbow.pitch", 0.0, 1.0),     # Straighten elbow
                ("shoulder.pitch", 0.0, 1.0),  # Lower arm
            ]
            
            for joint_name, position, duration in movements:
                if joint_name in robot_arm.joints:
                    robot_arm.joints[joint_name].goal_position = position
                    time.sleep(duration)
            
            logger.info("Wave gesture completed")
            return True
            
        except Exception as e:
            logger.error(f"Error performing wave gesture: {e}")
            return False


def main():
    """Main application entry point"""
    print("=== Reachy2 Robot Controller ===")
    
    # Initialize controller with simulation host
    controller = ReachyController(host="localhost")
    
    try:
        # Connect to robot
        if not controller.connect():
            print("Failed to connect to Reachy2. Check if simulation is running.")
            return
        
        # Get robot information
        print("\n--- Robot Information ---")
        info = controller.get_robot_info()
        for key, value in info.items():
            print(f"{key}: {value}")
        
        # Read joint positions
        print("\n--- Current Joint Positions ---")
        positions = controller.read_joint_positions()
        for part, joints in positions.items():
            if isinstance(joints, dict):
                print(f"\n{part.upper()}:")
                for joint_name, position in joints.items():
                    print(f"  {joint_name}: {position:.3f} rad")
        
        # Demonstrate robot movements
        print("\n--- Demonstrating Robot Movements ---")
        
        # Perform wave gesture
        print("Performing wave gesture...")
        if controller.wave_hello("r_arm"):
            print("[SUCCESS] Wave gesture completed successfully")
        else:
            print("[FAILED] Wave gesture failed")
        
        time.sleep(1)
        
        # Move to neutral position
        print("Moving to neutral position...")
        if controller.move_to_neutral_position():
            print("[SUCCESS] Robot moved to neutral position")
        else:
            print("[FAILED] Failed to move to neutral position")
        
        # Keep connection alive
        print("\nDemo completed. Press Ctrl+C to exit.")
        time.sleep(2)
        
    except KeyboardInterrupt:
        print("\nShutting down...")
    except Exception as e:
        logger.error(f"Application error: {e}")
    finally:
        controller.disconnect()


if __name__ == "__main__":
    main()