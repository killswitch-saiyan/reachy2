# Reachy2 Audio Troubleshooting Guide

## Common Audio Issues and Solutions

### 🔇 No Audio Output (Can't hear playback)

**Likely Causes:**
1. **Docker audio port not mapped** - Port 50063 missing
2. **Host audio system issues**
3. **Audio file format problems**
4. **MuJoCo container audio configuration**

**Solutions:**

#### 1. Check Docker Port Mapping
Ensure your Docker run command includes audio port:
```bash
docker run -p 50063:50063 -p 50051:50051 -p 6080:6080 reachy2_mujoco
```

#### 2. Test Audio System
```python
# Run this test in the enhanced audio system (option 16)
# Choose option 8: "Test recording & playback"
```

#### 3. Check Container Audio
```bash
# Inside container, test audio devices
docker exec reachy2_mujoco aplay -l
docker exec reachy2_mujoco arecord -l
```

#### 4. Host Audio Configuration (Windows)
- Ensure Windows audio is working
- Check volume levels
- Try different audio devices

### 🎙️ Recording Issues

**Symptoms:**
- Recording appears to work but no file created
- Recording files are empty or corrupted

**Solutions:**

#### 1. Check Microphone Access
- Ensure Docker container has microphone access
- Check Windows privacy settings for microphone

#### 2. Use Only .ogg Format for Recording
```python
# ✅ Correct - recording only supports .ogg
audio.record_audio("my_recording.ogg", duration_secs=5)

# ❌ Wrong - other formats not supported for recording
audio.record_audio("my_recording.wav", duration_secs=5)
```

#### 3. Test Recording Step-by-Step
```python
from audio import AudioManager
from main import ReachyController

controller = ReachyController(host="localhost")
controller.connect()
audio = AudioManager(controller.reachy)

# Test 1: List initial files
print("Before:", audio.list_audio_files())

# Test 2: Record
audio.record_audio("test", 3, countdown=False)

# Test 3: Check if file exists
print("After:", audio.list_audio_files())

# Test 4: Try playback
audio.play_audio_file("test.ogg")
```

### 📂 File Management Issues

#### Files Not Persisting
- **Issue**: Files disappear after container restart
- **Cause**: Audio files are stored in temporary container storage
- **Solution**: Download important recordings to host:
```python
audio.download_audio_file("important_recording.ogg", "C:/Users/YourName/Downloads")
```

#### Upload Failures
- **Supported formats**: .wav, .mp3, .ogg
- **Check file path**: Use absolute paths
- **File size**: Very large files may fail

### 🔊 Enhanced Audio System Features

The new AudioManager provides:

#### ✨ Improvements over Legacy System
1. **Better error handling** - Clear error messages
2. **File format validation** - Checks supported formats
3. **Interactive menu** - Easy-to-use interface
4. **Recording countdown** - Preparation time before recording
5. **File organization** - Lists files by type
6. **Automatic cleanup** - Test files removed after tests

#### 🎵 Usage Examples

**Quick Recording & Playback:**
```python
from audio import AudioManager

audio = AudioManager(reachy_sdk)

# Record 5-second clip
audio.record_audio("hello", 5)

# Play it back
audio.play_audio_file("hello.ogg")

# Download to computer
audio.download_audio_file("hello.ogg", "C:/Downloads")
```

**Interactive Menu:**
```python
# In interactive_demo.py, choose option 16
# Or run directly:
python test_audio.py
```

### 🐛 Debugging Steps

#### Step 1: Basic Connection
```python
from main import ReachyController
controller = ReachyController(host="localhost")
print("Connected:", controller.connect())
```

#### Step 2: Check Audio Server
```bash
# Should show audio server running on port 50063
docker exec reachy2_mujoco netstat -tlnp | grep 50063
```

#### Step 3: Test Raw Audio API
```python
# Direct SDK test
from reachy2_sdk import ReachySDK
reachy = ReachySDK(host="localhost")

# Test basic functions
print("Files:", reachy.audio.get_audio_files())
reachy.audio.record_audio("test.ogg", duration_secs=3)
print("After recording:", reachy.audio.get_audio_files())
```

#### Step 4: Check Container Logs
```bash
docker logs reachy2_mujoco | grep -i audio
```

### 📞 Getting Help

If audio still doesn't work:

1. **Check ports**: Ensure all required ports are mapped:
   - 50051 (main SDK)
   - 50063 (audio)
   - 6080 (VNC)

2. **Restart container**: Sometimes audio initialization fails
   ```bash
   docker restart reachy2_mujoco
   ```

3. **Try simple test**: Use the built-in audio test (option 8 in enhanced audio menu)

4. **Check documentation**: Visit [Pollen Robotics Audio Docs](https://docs.pollen-robotics.com/developing-with-reachy-2/basics/9-play-record-sound/)

## Success Indicators

✅ **Audio Working Correctly:**
- Files listed in `audio.list_audio_files()`
- Recording creates files visible in file list
- Playback produces audible sound
- Download saves files to host computer

❌ **Audio Not Working:**
- Empty file lists after recording
- No sound during playback
- Connection errors to audio server
- Recording files are 0 bytes