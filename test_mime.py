#!/usr/bin/env python3
"""
Test script for mime performance
Tests basic mime movements without full performance
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from main import ReachyController
from mime_performance import MimePerformer

def test_mime_basics():
    """Test basic mime setup and movements"""
    print("Testing Mime Performance Basics")
    print("=" * 40)
    
    # Initialize controller
    controller = ReachyController(host="localhost")
    
    try:
        print("Connecting to Reachy2...")
        if not controller.connect():
            print("❌ Failed to connect to Reachy2")
            return
        
        print("✅ Connected successfully!")
        
        # Initialize mime performer
        mime = MimePerformer(controller.reachy)
        
        print("\n🎭 Testing mime setup...")
        if mime._setup_mime_position():
            print("✅ Mime setup successful!")
            
            print("\n🔍 Testing rope discovery...")
            if mime._discover_rope():
                print("✅ Rope discovery successful!")
                
                print("\n🪢 Testing single rope pull...")
                if mime._pull_rope_sequence(use_right_arm=True):
                    print("✅ Rope pull successful!")
                else:
                    print("❌ Rope pull failed")
            else:
                print("❌ Rope discovery failed")
        else:
            print("❌ Mime setup failed")
        
        print("\n🏠 Returning to neutral...")
        mime._return_to_neutral()
        
    except Exception as e:
        print(f"❌ Test error: {e}")
    finally:
        controller.disconnect()
        print("Disconnected from robot.")

def test_mime_wall():
    """Test invisible wall performance"""
    print("\nTesting Invisible Wall Performance")
    print("=" * 40)
    
    # Initialize controller
    controller = ReachyController(host="localhost")
    
    try:
        print("Connecting to Reachy2...")
        if not controller.connect():
            print("❌ Failed to connect to Reachy2")
            return
        
        print("✅ Connected successfully!")
        
        # Initialize mime performer
        mime = MimePerformer(controller.reachy)
        
        print("\n🧱 Testing invisible wall...")
        if mime.perform_invisible_wall():
            print("✅ Invisible wall performance successful!")
        else:
            print("❌ Invisible wall performance failed")
        
    except Exception as e:
        print(f"❌ Test error: {e}")
    finally:
        controller.disconnect()
        print("Disconnected from robot.")

def main():
    """Main test function"""
    print("Reachy2 Mime Performance Test")
    print("=" * 50)
    print("Make sure your MuJoCo container is running!")
    print("View at: http://localhost:6080/vnc.html")
    print()
    
    choice = input("Test: (1) Basic mime movements, (2) Invisible wall, (3) Both: ")
    
    if choice == '1':
        test_mime_basics()
    elif choice == '2':  
        test_mime_wall()
    elif choice == '3':
        test_mime_basics()
        print("\n" + "="*50)
        test_mime_wall()
    else:
        print("Invalid choice")

if __name__ == "__main__":
    main()