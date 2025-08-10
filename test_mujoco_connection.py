#!/usr/bin/env python3
"""
Test script for MuJoCo connection
"""

from reachy2_sdk import ReachySDK
import time
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def test_mujoco_connection():
    """Test connection to MuJoCo simulation"""
    print("🔍 Testing MuJoCo Connection...")
    print("=" * 40)
    
    max_retries = 5
    retry_delay = 10
    
    for attempt in range(max_retries):
        try:
            print(f"Attempt {attempt + 1}/{max_retries}")
            print("Connecting to Reachy2 MuJoCo simulation...")
            
            # Create SDK connection
            reachy = ReachySDK(host='localhost')
            
            # Wait for connection to stabilize
            time.sleep(3)
            
            # Test basic connection
            print("Testing basic connection...")
            info = reachy.info
            print(f"✅ Robot info: {info}")
            
            # Test if robot is connected
            print(f"✅ Is connected: {reachy.is_connected}")
            
            # Test parts availability
            print("Testing parts availability...")
            if hasattr(reachy, 'head'):
                print("✅ Head available")
            if hasattr(reachy, 'r_arm'):
                print("✅ Right arm available")
            if hasattr(reachy, 'l_arm'):
                print("✅ Left arm available")
            
            # Test basic movement
            print("Testing basic head movement...")
            reachy.head.turn_on()
            time.sleep(1)
            
            # Simple head movement test
            reachy.head.look_at(x=0.5, y=0, z=0.1, duration=1.0, wait=True)
            print("✅ Head movement successful!")
            
            print("\n🎉 MuJoCo connection working perfectly!")
            print("You can now run: python interactive_demo.py")
            
            reachy.disconnect()
            return True
            
        except Exception as e:
            print(f"❌ Attempt {attempt + 1} failed: {e}")
            if attempt < max_retries - 1:
                print(f"Waiting {retry_delay} seconds before retry...")
                time.sleep(retry_delay)
            else:
                print("\n💡 Troubleshooting suggestions:")
                print("1. Make sure Docker container is fully started (wait 2-3 minutes)")
                print("2. Check container logs: docker logs reachy2_mujoco")
                print("3. Verify ports are accessible: netstat -an | findstr :50051")
                print("4. Try restarting the container")
    
    return False

if __name__ == "__main__":
    test_mujoco_connection()