# 🍽️ Canteen Occupancy Monitor

A real-time web application that displays the number of people currently in a canteen, helping visitors decide the best time to visit. The app fetches data from ThingSpeak IoT cloud and provides a beautiful, responsive interface with Tailwind CSS.

## ✨ Features

- **Real-time Data**: Fetches occupancy data from ThingSpeak IoT cloud
- **Beautiful UI**: Modern, responsive design with Tailwind CSS
- **Traffic Indicators**: Color-coded status (Green/Yellow/Red) based on occupancy
- **Auto Refresh**: Automatic data updates every 30 seconds
- **Manual Refresh**: Manual refresh button for immediate updates
- **Recommendations**: Smart suggestions based on current occupancy
- **Mobile Friendly**: Responsive design that works on all devices

## 🚀 Quick Start

### Prerequisites

- Python 3.7 or higher
- ThingSpeak account and channel
- Internet connection

### Installation

1. **Clone or download this repository**
   ```bash
   git clone <repository-url>
   cd canteen-occupancy-monitor
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure ThingSpeak**
   
   Create a `.env` file in the project root:
   ```bash
   # ThingSpeak Configuration
   THINGSPEAK_CHANNEL_ID=your_channel_id
   THINGSPEAK_API_KEY=your_write_api_key
   THINGSPEAK_READ_API_KEY=your_read_api_key
   ```

4. **Run the application**
   ```bash
   python app.py
   ```

5. **Open your browser**
   Navigate to `http://localhost:5000`

## 🔧 ThingSpeak Setup

### Creating a ThingSpeak Channel

1. Go to [ThingSpeak.com](https://thingspeak.com) and create an account
2. Create a new channel:
   - Name: "Canteen Occupancy"
   - Field 1: "People Count" (or similar)
   - Make the channel public or note down the Read API Key
3. Note down your Channel ID and API Keys

### Sending Data to ThingSpeak

You can send occupancy data to ThingSpeak using various methods:

#### Method 1: HTTP GET Request
```bash
curl "https://api.thingspeak.com/update?api_key=YOUR_WRITE_API_KEY&field1=15"
```

#### Method 2: Python Script
```python
import requests

def update_occupancy(count):
    url = "https://api.thingspeak.com/update"
    params = {
        'api_key': 'YOUR_WRITE_API_KEY',
        'field1': count
    }
    response = requests.get(url, params=params)
    return response.status_code == 200

# Example usage
update_occupancy(15)  # Update with 15 people
```

#### Method 3: Arduino/ESP32 Example
```cpp
#include <WiFi.h>
#include <HTTPClient.h>

const char* ssid = "YOUR_WIFI_SSID";
const char* password = "YOUR_WIFI_PASSWORD";
const char* thingspeak_api_key = "YOUR_WRITE_API_KEY";

void setup() {
  Serial.begin(115200);
  WiFi.begin(ssid, password);
  
  while (WiFi.status() != WL_CONNECTED) {
    delay(1000);
    Serial.println("Connecting to WiFi...");
  }
}

void loop() {
  if (WiFi.status() == WL_CONNECTED) {
    HTTPClient http;
    String url = "https://api.thingspeak.com/update?api_key=" + String(thingspeak_api_key) + "&field1=" + String(getPeopleCount());
    
    http.begin(url);
    int httpResponseCode = http.GET();
    
    if (httpResponseCode > 0) {
      Serial.println("Data sent successfully");
    } else {
      Serial.println("Error sending data");
    }
    
    http.end();
  }
  
  delay(30000); // Send data every 30 seconds
}

int getPeopleCount() {
  // Your sensor logic here
  // This could be from PIR sensors, ultrasonic sensors, etc.
  return 15; // Example value
}
```

## 📊 Traffic Levels

The app categorizes occupancy into three levels:

- **🟢 Low Traffic (0-10 people)**: Great time to visit
- **🟡 Moderate Traffic (11-25 people)**: Decent time to visit  
- **🔴 High Traffic (26+ people)**: Consider waiting

## 🛠️ Configuration

### Environment Variables

Create a `.env` file with the following variables:

```env
# ThingSpeak Configuration
THINGSPEAK_CHANNEL_ID=1234567
THINGSPEAK_API_KEY=ABC123XYZ789
THINGSPEAK_READ_API_KEY=DEF456UVW012

# Optional Configuration
SECRET_KEY=your-secret-key
DEBUG=True
REFRESH_INTERVAL=30
```

### Customizing Field Names

If your ThingSpeak channel uses different field names, update the `get_thingspeak_data()` function in `app.py`:

```python
# Change 'field1' to your actual field name
occupancy_count = int(data.get('field2', 0))  # Using field2 instead
```

## 🌐 API Endpoints

- `GET /` - Main dashboard page
- `GET /api/occupancy` - JSON data for current occupancy
- `GET /api/status` - Health check endpoint

## 🎨 Customization

### Changing Colors

Edit the Tailwind configuration in `templates/index.html`:

```javascript
tailwind.config = {
    theme: {
        extend: {
            colors: {
                'canteen-green': '#10B981',  // Change these colors
                'canteen-red': '#EF4444',
                'canteen-yellow': '#F59E0B'
            }
        }
    }
}
```

### Modifying Traffic Thresholds

Update the JavaScript in `templates/index.html`:

```javascript
if (count <= 10) {
    // Low traffic
} else if (count <= 25) {
    // Moderate traffic  
} else {
    // High traffic
}
```

## 🚀 Deployment

### Local Development
```bash
python app.py
```

### Production Deployment

#### Using Gunicorn
```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

#### Using Docker
```dockerfile
FROM python:3.9-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
EXPOSE 5000

CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "app:app"]
```

## 🔍 Troubleshooting

### Common Issues

1. **"Connection Error" displayed**
   - Check your internet connection
   - Verify ThingSpeak API keys are correct
   - Ensure the channel ID is valid

2. **Data not updating**
   - Check if data is being sent to ThingSpeak
   - Verify the field name matches your channel setup
   - Check ThingSpeak channel permissions

3. **App won't start**
   - Ensure all dependencies are installed: `pip install -r requirements.txt`
   - Check Python version (3.7+ required)
   - Verify all files are in the correct locations

### Debug Mode

Enable debug mode by setting `DEBUG=True` in your `.env` file or running:
```bash
export DEBUG=True
python app.py
```

## 📱 Mobile Usage

The app is fully responsive and works great on mobile devices. You can:

- Bookmark the URL for quick access
- Add to home screen for app-like experience
- Use auto-refresh for hands-free monitoring

## 🤝 Contributing

Feel free to submit issues, feature requests, or pull requests to improve this application.

## 📄 License

This project is open source and available under the MIT License.

## 🙏 Acknowledgments

- [ThingSpeak](https://thingspeak.com) for IoT data hosting
- [Tailwind CSS](https://tailwindcss.com) for beautiful styling
- [Flask](https://flask.palletsprojects.com/) for the web framework
