#!/usr/bin/env python3
"""
Test script for ThingSpeak integration
This script simulates sending occupancy data to ThingSpeak
"""

import requests
import time
import random
from config import Config

def send_occupancy_data(count):
    """Send occupancy count to ThingSpeak"""
    url = "https://api.thingspeak.com/update"
    params = {
        'api_key': Config.THINGSPEAK_API_KEY,
        'field1': count
    }
    
    try:
        response = requests.get(url, params=params, timeout=10)
        if response.status_code == 200:
            print(f"✅ Successfully sent occupancy count: {count}")
            return True
        else:
            print(f"❌ Failed to send data. Status code: {response.status_code}")
            return False
    except requests.exceptions.RequestException as e:
        print(f"❌ Error sending data: {e}")
        return False

def get_occupancy_data():
    """Get latest occupancy data from ThingSpeak"""
    url = f"https://api.thingspeak.com/channels/{Config.THINGSPEAK_CHANNEL_ID}/feeds/last.json"
    params = {
        'api_key': Config.THINGSPEAK_READ_API_KEY
    }
    
    try:
        response = requests.get(url, params=params, timeout=10)
        if response.status_code == 200:
            data = response.json()
            count = data.get('field1', 'N/A')
            timestamp = data.get('created_at', 'N/A')
            print(f"📊 Latest occupancy: {count} people (Updated: {timestamp})")
            return data
        else:
            print(f"❌ Failed to get data. Status code: {response.status_code}")
            return None
    except requests.exceptions.RequestException as e:
        print(f"❌ Error getting data: {e}")
        return None

def simulate_canteen_traffic():
    """Simulate realistic canteen traffic patterns"""
    print("🍽️ Canteen Occupancy Simulator")
    print("=" * 40)
    
    # Simulate different times of day
    scenarios = [
        ("Morning Rush (8-9 AM)", 25, 35),
        ("Mid-Morning (9-11 AM)", 5, 15),
        ("Lunch Peak (12-1 PM)", 30, 45),
        ("Afternoon (2-4 PM)", 8, 18),
        ("Evening (5-6 PM)", 20, 30),
        ("Night (7-9 PM)", 3, 10)
    ]
    
    for scenario_name, min_count, max_count in scenarios:
        print(f"\n📅 {scenario_name}")
        print("-" * 30)
        
        # Send 3-5 data points for each scenario
        for i in range(random.randint(3, 5)):
            count = random.randint(min_count, max_count)
            send_occupancy_data(count)
            time.sleep(2)  # Wait 2 seconds between updates
    
    print("\n✅ Simulation completed!")

def main():
    """Main function"""
    print("ThingSpeak Test Script")
    print("=" * 20)
    
    # Check configuration
    if Config.THINGSPEAK_CHANNEL_ID == 'YOUR_CHANNEL_ID':
        print("❌ Please configure your ThingSpeak credentials in .env file")
        print("   Copy .env.example to .env and fill in your values")
        return
    
    while True:
        print("\nChoose an option:")
        print("1. Send test data (random count)")
        print("2. Get latest data")
        print("3. Simulate canteen traffic")
        print("4. Send custom count")
        print("5. Exit")
        
        choice = input("\nEnter your choice (1-5): ").strip()
        
        if choice == '1':
            count = random.randint(0, 50)
            send_occupancy_data(count)
            
        elif choice == '2':
            get_occupancy_data()
            
        elif choice == '3':
            simulate_canteen_traffic()
            
        elif choice == '4':
            try:
                count = int(input("Enter occupancy count: "))
                send_occupancy_data(count)
            except ValueError:
                print("❌ Please enter a valid number")
                
        elif choice == '5':
            print("👋 Goodbye!")
            break
            
        else:
            print("❌ Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
