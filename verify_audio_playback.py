#!/usr/bin/env python3
"""
Audio Playback Verification Script
Tests if you can actually hear the audio playback
"""

import sys
import os
import time
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from main import ReachyController
from audio import AudioManager

def verify_audio_playback():
    """Verify audio playback is actually working"""
    print("🔊 Audio Playback Verification Test")
    print("=" * 50)
    
    controller = ReachyController(host="localhost")
    
    try:
        if not controller.connect():
            print("❌ Failed to connect to Reachy2")
            return
        
        audio = AudioManager(controller.reachy)
        
        print("Step 1: Recording a clear test message...")
        print("When recording starts, say 'HELLO WORLD' loudly and clearly")
        
        if audio.record_audio("playback_test", duration_secs=5, countdown=True):
            print("\n✅ Recording completed!")
            
            print("\nStep 2: Playing back recording...")
            print("🎧 LISTEN CAREFULLY - You should hear your voice now!")
            print("💡 Make sure your computer speakers/headphones are on and volume up!")
            
            # Play with extended monitoring
            if audio.play_audio_file("playback_test.ogg"):
                print("\n⏱️ Playing for 8 seconds... LISTEN!")
                
                # Give plenty of time to hear
                for i in range(8):
                    print(f"   Second {i+1}/8 - Can you hear your voice?")
                    time.sleep(1)
                
                print("\n❓ Did you hear your recorded voice playing back?")
                heard_audio = input("Enter 'y' if you heard audio, 'n' if no sound: ").strip().lower()
                
                if heard_audio.startswith('y'):
                    print("🎉 AUDIO SYSTEM FULLY WORKING!")
                    print("✅ Recording: Working")
                    print("✅ File storage: Working") 
                    print("✅ Playback: Working")
                    print("✅ Audio output: Working")
                else:
                    print("\n🔧 AUDIO OUTPUT ISSUE DETECTED")
                    print("Recording and file management work, but no audio output")
                    print("\nTroubleshooting steps:")
                    print("1. Check if Docker port 50063 is mapped correctly")
                    print("2. Verify your computer's audio output is working")
                    print("3. Check volume levels (both system and application)")
                    print("4. Try different audio output device")
                    
                    # Additional diagnostics
                    print("\n🔍 Diagnostics:")
                    files = audio.list_audio_files()
                    print(f"Files on robot: {files}")
                    
                    if "playback_test.ogg" in files:
                        download_test = input("Download file to test locally? (y/n): ").strip().lower()
                        if download_test.startswith('y'):
                            print("Downloading to current directory...")
                            if audio.download_audio_file("playback_test.ogg", "./"):
                                print("✅ Downloaded! Try playing 'playback_test.ogg' locally")
            
            # Cleanup
            print("\nCleaning up test file...")
            audio.remove_audio_file("playback_test.ogg", confirm=False)
            
        else:
            print("❌ Recording failed - check microphone access")
    
    except Exception as e:
        print(f"❌ Test error: {e}")
    finally:
        controller.disconnect()

if __name__ == "__main__":
    verify_audio_playback()