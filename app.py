from flask import Flask, render_template, jsonify
import requests
import os
from datetime import datetime
import time
from config import Config

app = Flask(__name__)
app.config.from_object(Config)

# ThingSpeak configuration
THINGSPEAK_CHANNEL_ID = app.config['THINGSPEAK_CHANNEL_ID']
THINGSPEAK_API_KEY = app.config['THINGSPEAK_API_KEY']
THINGSPEAK_READ_API_KEY = app.config['THINGSPEAK_READ_API_KEY']

def get_thingspeak_data():
    """
    Fetch data from ThingSpeak channel
    Returns the latest occupancy count
    """
    try:
        # ThingSpeak API endpoint for getting latest data
        url = f"https://api.thingspeak.com/channels/{THINGSPEAK_CHANNEL_ID}/feeds/last.json"
        params = {
            'api_key': THINGSPEAK_READ_API_KEY
        }
        
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        
        data = response.json()
        
        # Assuming field1 contains the occupancy count
        # Adjust field name based on your ThingSpeak channel setup
        occupancy_count = int(data.get('field1', 0))
        last_updated = data.get('created_at', '')
        
        return {
            'occupancy': occupancy_count,
            'last_updated': last_updated,
            'status': 'success'
        }
        
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data from ThingSpeak: {e}")
        return {
            'occupancy': 0,
            'last_updated': '',
            'status': 'error',
            'error': str(e)
        }
    except Exception as e:
        print(f"Unexpected error: {e}")
        return {
            'occupancy': 0,
            'last_updated': '',
            'status': 'error',
            'error': str(e)
        }

@app.route('/')
def index():
    """Main page displaying canteen occupancy"""
    data = get_thingspeak_data()
    return render_template('index.html', data=data)

@app.route('/api/occupancy')
def api_occupancy():
    """API endpoint for getting current occupancy data"""
    data = get_thingspeak_data()
    return jsonify(data)

@app.route('/api/status')
def api_status():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
        'thingspeak_channel': THINGSPEAK_CHANNEL_ID
    })

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5002)
