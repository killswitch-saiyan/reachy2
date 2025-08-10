# Reachy2 Robot Project

A Python application for controlling and interacting with the Reachy2 robot using the official SDK.

## Setup

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Make sure your Reachy2 simulation is running at `http://localhost:6080`

3. Run the main application:
   ```bash
   python main.py
   ```

## Features

- Connect to Reachy2 robot (simulation or real hardware)
- Read robot status and joint positions
- Safe connection handling with error recovery
- Extensible controller class for additional functionality

## Project Structure

- `main.py` - Main application entry point
- `requirements.txt` - Python dependencies
- `README.md` - Project documentation