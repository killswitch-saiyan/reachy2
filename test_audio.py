#!/usr/bin/env python3
"""
Test script for enhanced audio functionality
Tests the new AudioManager class
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from main import ReachyController
from audio import AudioManager

def test_audio_basic():
    """Test basic audio functionality"""
    print("Testing Enhanced Audio System")
    print("=" * 40)
    
    # Initialize controller
    controller = ReachyController(host="localhost")
    
    try:
        print("Connecting to Reachy2...")
        if not controller.connect():
            print("❌ Failed to connect to Reachy2")
            return
        
        print("✅ Connected successfully!")
        
        # Initialize audio manager
        audio = AudioManager(controller.reachy)
        
        print("\n1. Testing file listing...")
        files = audio.list_audio_files()
        print(f"Found {len(files)} audio files: {files}")
        
        print("\n2. Testing recording...")
        if audio.record_audio("test_recording", duration_secs=3, countdown=True):
            print("✅ Recording test passed!")
            
            print("\n3. Testing playback...")
            if audio.play_audio_file("test_recording.ogg"):
                print("✅ Playback test passed!")
                
                # Wait for playback
                import time
                time.sleep(4)
                
                print("\n4. Testing file removal...")
                if audio.remove_audio_file("test_recording.ogg", confirm=False):
                    print("✅ File removal test passed!")
                else:
                    print("⚠️ File removal test failed")
            else:
                print("❌ Playback test failed")
        else:
            print("❌ Recording test failed")
        
        print("\n5. Testing file info...")
        info = audio.get_file_info()
        print(f"File info: {info}")
        
        print("\n✅ Audio system test completed!")
        
    except Exception as e:
        print(f"❌ Test error: {e}")
    finally:
        controller.disconnect()
        print("Disconnected from robot.")

def test_audio_interactive():
    """Test interactive audio menu"""
    print("\nTesting Interactive Audio Menu")
    print("=" * 40)
    
    # Initialize controller
    controller = ReachyController(host="localhost")
    
    try:
        print("Connecting to Reachy2...")
        if not controller.connect():
            print("❌ Failed to connect to Reachy2")
            return
        
        print("✅ Connected successfully!")
        
        # Initialize audio manager
        audio = AudioManager(controller.reachy)
        
        print("\nLaunching interactive audio menu...")
        audio.interactive_audio_menu()
        
    except Exception as e:
        print(f"❌ Test error: {e}")
    finally:
        controller.disconnect()
        print("Disconnected from robot.")

def main():
    """Main test function"""
    print("Reachy2 Enhanced Audio System Test")
    print("=" * 50)
    print("Make sure your MuJoCo container is running!")
    print("Audio issues? Check Docker port 50063 is mapped correctly")
    print()
    
    choice = input("Test: (1) Basic audio functions, (2) Interactive menu: ")
    
    if choice == '1':
        test_audio_basic()
    elif choice == '2':
        test_audio_interactive()
    else:
        print("Invalid choice")

if __name__ == "__main__":
    main()