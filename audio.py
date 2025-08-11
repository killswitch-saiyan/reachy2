#!/usr/bin/env python3
"""
Reachy2 Audio Management Module
Provides comprehensive audio recording, playback, and management functionality
Based on Pollen Robotics documentation and enhanced for better user experience
"""

import time
import logging
import os
from typing import List, Optional, Dict
from reachy2_sdk import ReachySDK

logger = logging.getLogger(__name__)

class AudioManager:
    """Enhanced audio management for Reachy2 robot"""
    
    def __init__(self, reachy_sdk: ReachySDK):
        """
        Initialize audio manager
        
        Args:
            reachy_sdk: Connected ReachySDK instance
        """
        self.reachy = reachy_sdk
        self.supported_formats = ['.wav', '.mp3', '.ogg']
        self.recording_format = '.ogg'  # Only format supported for recording
        
    def list_audio_files(self) -> List[str]:
        """
        List all audio files stored on the robot
        
        Returns:
            List of audio filenames
        """
        try:
            files = self.reachy.audio.get_audio_files()
            return files if files else []
        except Exception as e:
            logger.error(f"Failed to list audio files: {e}")
            return []
    
    def upload_audio_file(self, local_path: str) -> bool:
        """
        Upload an audio file to the robot
        
        Args:
            local_path: Path to local audio file
            
        Returns:
            bool: True if upload successful
        """
        try:
            if not os.path.exists(local_path):
                print(f"❌ File not found: {local_path}")
                return False
            
            # Check file format
            file_ext = os.path.splitext(local_path)[1].lower()
            if file_ext not in self.supported_formats:
                print(f"❌ Unsupported format: {file_ext}")
                print(f"Supported formats: {', '.join(self.supported_formats)}")
                return False
            
            print(f"📤 Uploading {os.path.basename(local_path)}...")
            self.reachy.audio.upload_audio_file(local_path)
            print(f"✅ Upload completed: {os.path.basename(local_path)}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to upload audio file: {e}")
            print(f"❌ Upload failed: {e}")
            return False
    
    def play_audio_file(self, filename: str, wait_for_completion: bool = False) -> bool:
        """
        Play an audio file stored on the robot
        
        Args:
            filename: Name of audio file to play
            wait_for_completion: If True, wait for playback to complete
            
        Returns:
            bool: True if playback started successfully
        """
        try:
            # Check if file exists
            available_files = self.list_audio_files()
            if filename not in available_files:
                print(f"❌ Audio file not found: {filename}")
                print(f"Available files: {', '.join(available_files) if available_files else 'None'}")
                return False
            
            print(f"🔊 Playing: {filename}")
            self.reachy.audio.play_audio_file(filename)
            
            if wait_for_completion:
                print("Waiting for playback to complete...")
                print("Press Ctrl+C to stop playback early")
                try:
                    # Wait for user to stop or natural completion
                    while True:
                        time.sleep(0.5)
                except KeyboardInterrupt:
                    print("\n⏹️ Stopping playback...")
                    self.stop_playback()
            
            return True
            
        except Exception as e:
            logger.error(f"Failed to play audio file: {e}")
            print(f"❌ Playback failed: {e}")
            return False
    
    def stop_playback(self) -> bool:
        """
        Stop current audio playback
        
        Returns:
            bool: True if stop successful
        """
        try:
            self.reachy.audio.stop_playing()
            print("⏹️ Playback stopped")
            return True
        except Exception as e:
            logger.error(f"Failed to stop playback: {e}")
            print(f"❌ Stop failed: {e}")
            return False
    
    def record_audio(self, filename: str, duration_secs: int = 5, 
                    countdown: bool = True) -> bool:
        """
        Record audio using robot's microphone
        
        Args:
            filename: Name for recorded file (will add .ogg if missing)
            duration_secs: Recording duration in seconds
            countdown: If True, show countdown before recording
            
        Returns:
            bool: True if recording successful
        """
        try:
            # Ensure .ogg extension
            if not filename.endswith('.ogg'):
                filename += '.ogg'
            
            if countdown and duration_secs > 3:
                print("🎙️ Preparing to record...")
                for i in range(3, 0, -1):
                    print(f"Starting in {i}...")
                    time.sleep(1)
            
            print(f"🔴 Recording '{filename}' for {duration_secs} seconds...")
            print("Speak now!")
            
            self.reachy.audio.record_audio(filename, duration_secs=duration_secs)
            
            # Wait for recording to complete plus buffer
            time.sleep(duration_secs + 1)
            
            print(f"✅ Recording completed: {filename}")
            
            # Verify file was created
            files = self.list_audio_files()
            if filename in files:
                print(f"✅ File confirmed in robot storage")
                return True
            else:
                print(f"⚠️ File may not have been saved properly")
                return False
            
        except Exception as e:
            logger.error(f"Failed to record audio: {e}")
            print(f"❌ Recording failed: {e}")
            return False
    
    def stop_recording(self) -> bool:
        """
        Stop current audio recording
        
        Returns:
            bool: True if stop successful
        """
        try:
            self.reachy.audio.stop_recording()
            print("⏹️ Recording stopped")
            return True
        except Exception as e:
            logger.error(f"Failed to stop recording: {e}")
            print(f"❌ Stop recording failed: {e}")
            return False
    
    def download_audio_file(self, filename: str, local_path: str) -> bool:
        """
        Download an audio file from the robot
        
        Args:
            filename: Name of file on robot
            local_path: Local path to save file
            
        Returns:
            bool: True if download successful
        """
        try:
            # Check if file exists on robot
            available_files = self.list_audio_files()
            if filename not in available_files:
                print(f"❌ File not found on robot: {filename}")
                return False
            
            print(f"📥 Downloading {filename}...")
            self.reachy.audio.download_audio_file(filename, local_path)
            
            # Verify local file was created
            full_path = os.path.join(local_path, filename)
            if os.path.exists(full_path):
                print(f"✅ Downloaded to: {full_path}")
                return True
            else:
                print(f"⚠️ Download may have failed")
                return False
            
        except Exception as e:
            logger.error(f"Failed to download audio file: {e}")
            print(f"❌ Download failed: {e}")
            return False
    
    def remove_audio_file(self, filename: str, confirm: bool = True) -> bool:
        """
        Remove an audio file from the robot
        
        Args:
            filename: Name of file to remove
            confirm: If True, ask for confirmation
            
        Returns:
            bool: True if removal successful
        """
        try:
            # Check if file exists
            available_files = self.list_audio_files()
            if filename not in available_files:
                print(f"❌ File not found: {filename}")
                return False
            
            if confirm:
                response = input(f"Are you sure you want to delete '{filename}'? (y/N): ")
                if not response.lower().startswith('y'):
                    print("Delete cancelled")
                    return False
            
            self.reachy.audio.remove_audio_file(filename)
            print(f"🗑️ Removed: {filename}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to remove audio file: {e}")
            print(f"❌ Removal failed: {e}")
            return False
    
    def get_file_info(self) -> Dict[str, List[str]]:
        """
        Get organized information about audio files
        
        Returns:
            Dictionary with file info organized by type
        """
        files = self.list_audio_files()
        info = {
            'wav': [],
            'mp3': [],
            'ogg': [],
            'other': []
        }
        
        for file in files:
            ext = os.path.splitext(file)[1].lower()
            if ext == '.wav':
                info['wav'].append(file)
            elif ext == '.mp3':
                info['mp3'].append(file)
            elif ext == '.ogg':
                info['ogg'].append(file)
            else:
                info['other'].append(file)
        
        return info
    
    def interactive_audio_menu(self):
        """Interactive audio management menu"""
        while True:
            print("\n" + "=" * 40)
            print("🎵 REACHY2 AUDIO MANAGER")
            print("=" * 40)
            print("1. List audio files")
            print("2. Upload audio file")
            print("3. Play audio file")
            print("4. Record new audio")
            print("5. Download audio file")
            print("6. Remove audio file")
            print("7. Stop playback/recording")
            print("8. Test recording & playback")
            print("9. Back to main menu")
            
            choice = input("\nEnter choice (1-9): ").strip()
            
            try:
                if choice == '1':
                    self._menu_list_files()
                elif choice == '2':
                    self._menu_upload_file()
                elif choice == '3':
                    self._menu_play_file()
                elif choice == '4':
                    self._menu_record_audio()
                elif choice == '5':
                    self._menu_download_file()
                elif choice == '6':
                    self._menu_remove_file()
                elif choice == '7':
                    self._menu_stop_audio()
                elif choice == '8':
                    self._menu_test_audio()
                elif choice == '9':
                    break
                else:
                    print("Invalid choice. Please enter 1-9.")
                    
            except Exception as e:
                print(f"❌ Error: {e}")
    
    def _menu_list_files(self):
        """Menu option: List files"""
        print("\n📋 Audio Files on Robot:")
        info = self.get_file_info()
        
        total_files = sum(len(files) for files in info.values())
        if total_files == 0:
            print("No audio files found")
            return
        
        for file_type, files in info.items():
            if files:
                print(f"\n{file_type.upper()} files:")
                for i, file in enumerate(files, 1):
                    print(f"  {i}. {file}")
        
        print(f"\nTotal: {total_files} files")
    
    def _menu_upload_file(self):
        """Menu option: Upload file"""
        file_path = input("Enter full path to audio file: ").strip()
        if file_path:
            self.upload_audio_file(file_path)
    
    def _menu_play_file(self):
        """Menu option: Play file"""
        files = self.list_audio_files()
        if not files:
            print("No audio files available")
            return
        
        print("\nAvailable files:")
        for i, file in enumerate(files, 1):
            print(f"{i}. {file}")
        
        choice = input("Enter filename or number: ").strip()
        
        # Handle numeric choice
        try:
            file_index = int(choice) - 1
            if 0 <= file_index < len(files):
                filename = files[file_index]
            else:
                print("Invalid number")
                return
        except ValueError:
            filename = choice
        
        wait = input("Wait for completion? (y/N): ").strip().lower()
        self.play_audio_file(filename, wait_for_completion=wait.startswith('y'))
    
    def _menu_record_audio(self):
        """Menu option: Record audio"""
        filename = input("Enter filename for recording (without extension): ").strip()
        if not filename:
            print("Filename required")
            return
        
        duration = input("Duration in seconds (default: 5): ").strip()
        try:
            duration = int(duration) if duration else 5
        except ValueError:
            duration = 5
        
        self.record_audio(filename, duration)
    
    def _menu_download_file(self):
        """Menu option: Download file"""
        files = self.list_audio_files()
        if not files:
            print("No audio files available")
            return
        
        print("\nAvailable files:")
        for i, file in enumerate(files, 1):
            print(f"{i}. {file}")
        
        filename = input("Enter filename to download: ").strip()
        local_path = input("Enter local directory path (default: C:/): ").strip()
        
        if not local_path:
            local_path = "C:/"
        
        self.download_audio_file(filename, local_path)
    
    def _menu_remove_file(self):
        """Menu option: Remove file"""
        files = self.list_audio_files()
        if not files:
            print("No audio files available")
            return
        
        print("\nAvailable files:")
        for i, file in enumerate(files, 1):
            print(f"{i}. {file}")
        
        filename = input("Enter filename to remove: ").strip()
        self.remove_audio_file(filename)
    
    def _menu_stop_audio(self):
        """Menu option: Stop audio"""
        print("Stopping all audio operations...")
        self.stop_playback()
        self.stop_recording()
    
    def _menu_test_audio(self):
        """Menu option: Test audio system"""
        print("\n🧪 Audio System Test")
        test_filename = "audio_test"
        
        print("Step 1: Recording 3-second test...")
        if self.record_audio(test_filename, 3):
            print("Step 2: Playing back recording...")
            time.sleep(1)
            if self.play_audio_file(test_filename + ".ogg"):
                time.sleep(4)  # Let it play
                print("Step 3: Cleaning up...")
                self.remove_audio_file(test_filename + ".ogg", confirm=False)
                print("✅ Audio test completed!")
            else:
                print("❌ Playback test failed")
        else:
            print("❌ Recording test failed")

def demo_audio_system(controller):
    """Demo function for audio system"""
    print("\n🎵 Reachy2 Audio System")
    print("Enhanced audio recording and playback")
    
    try:
        audio_manager = AudioManager(controller.reachy)
        audio_manager.interactive_audio_menu()
        
    except Exception as e:
        print(f"❌ Audio system error: {e}")

if __name__ == "__main__":
    # Standalone testing
    from main import ReachyController
    
    print("Reachy2 Audio Manager Test")
    controller = ReachyController(host="localhost")
    
    if controller.connect():
        demo_audio_system(controller)
        controller.disconnect()
    else:
        print("Failed to connect to robot")