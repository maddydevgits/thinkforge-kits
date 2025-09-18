import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Config:
    """Configuration class for the Flask app"""
    
    # ThingSpeak Configuration
    THINGSPEAK_CHANNEL_ID = os.getenv('THINGSPEAK_CHANNEL_ID', 'YOUR_CHANNEL_ID')
    THINGSPEAK_API_KEY = os.getenv('THINGSPEAK_API_KEY', 'YOUR_WRITE_API_KEY')
    THINGSPEAK_READ_API_KEY = os.getenv('THINGSPEAK_READ_API_KEY', 'YOUR_READ_API_KEY')
    
    # Flask Configuration
    SECRET_KEY = os.getenv('SECRET_KEY', 'your-secret-key-here')
    DEBUG = os.getenv('DEBUG', 'True').lower() == 'true'
    
    # App Configuration
    REFRESH_INTERVAL = int(os.getenv('REFRESH_INTERVAL', '30'))  # seconds
