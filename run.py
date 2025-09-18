#!/usr/bin/env python3
"""
Simple script to run the Canteen Occupancy Monitor
"""

import os
import sys
from app import app

def main():
    """Main function to run the Flask app"""
    print("🍽️ Starting Canteen Occupancy Monitor...")
    print("=" * 50)
    
    # Check if .env file exists
    if not os.path.exists('.env'):
        print("⚠️  Warning: .env file not found!")
        print("   Please create a .env file with your ThingSpeak credentials.")
        print("   Copy env_template.txt to .env and fill in your values.")
        print()
    
    # Check configuration
    from config import Config
    if Config.THINGSPEAK_CHANNEL_ID == 'YOUR_CHANNEL_ID':
        print("⚠️  Warning: ThingSpeak not configured!")
        print("   Please set up your ThingSpeak credentials in .env file.")
        print("   The app will run but won't be able to fetch real data.")
        print()
    
    print("🚀 Starting Flask development server...")
    print("📱 Open your browser and go to: http://localhost:5002")
    print("🛑 Press Ctrl+C to stop the server")
    print("=" * 50)
    
    try:
        app.run(debug=True, host='0.0.0.0', port=5002)
    except KeyboardInterrupt:
        print("\n👋 Server stopped. Goodbye!")
    except Exception as e:
        print(f"\n❌ Error starting server: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
