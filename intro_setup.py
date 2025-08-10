#!/usr/bin/env python3
"""
Standalone intro setup script for Reachy2
Performs the intro sequence: head down -> turn on -> head up
"""

import argparse
import logging
from main import ReachyController

logging.basicConfig(level=logging.INFO)

def main():
    """Standalone intro setup"""
    parser = argparse.ArgumentParser(description="Reachy2 Intro Setup")
    parser.add_argument('--host', default='localhost', help='Reachy host address')
    parser.add_argument('--speed', choices=['slow', 'medium', 'fast'], default='medium', 
                       help='Animation speed')
    parser.add_argument('--reset-only', action='store_true', 
                       help='Only reset to head-down position (no full intro)')
    
    args = parser.parse_args()
    
    print("🤖 Reachy2 Intro Setup")
    print("=" * 30)
    
    # Initialize controller
    controller = ReachyController(host=args.host)
    
    try:
        # Connect to robot
        if not controller.connect():
            print("❌ Failed to connect to Reachy2")
            return 1
        
        if args.reset_only:
            print("Resetting to head-down position...")
            if controller.reset_to_down_position():
                print("✅ Reset completed successfully!")
            else:
                print("❌ Reset failed")
                return 1
        else:
            print(f"Starting intro setup at {args.speed} speed...")
            print("Watch at: http://localhost:6080/vnc.html")
            
            if controller.perform_intro_setup(args.speed):
                print("✅ Intro setup completed successfully!")
                print("🎉 Reachy2 is ready for action!")
            else:
                print("❌ Intro setup failed")
                return 1
        
        return 0
        
    except KeyboardInterrupt:
        print("\n⏹️  Intro setup interrupted")
        return 1
    except Exception as e:
        print(f"❌ Error: {e}")
        return 1
    finally:
        controller.disconnect()

if __name__ == "__main__":
    exit(main())