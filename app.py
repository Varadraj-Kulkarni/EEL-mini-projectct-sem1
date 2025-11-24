from flask import Flask, render_template
import requests
from datetime import datetime, timezone
import pytz

app = Flask(__name__)

@app.route('/')
def home():
    # Fetch live data from USGS
    url = "https://earthquake.usgs.gov/fdsnws/event/1/query?format=geojson&latitude=22.0&longitude=78.0&maxradiuskm=1500&orderby=time"
    response = requests.get(url)
    data = response.json()

    earthquakes = []
    for feature in data['features']:
        mag = feature['properties']['mag']
        place = feature['properties']['place']
        local_tz = pytz.timezone("Asia/Kolkata")  # ← change to your timezone (e.g., "America/New_York")
        utc_time = datetime.fromtimestamp(feature['properties']['time'] / 1000, tz=timezone.utc)
        local_time = utc_time.astimezone(local_tz)
        time = local_time.strftime("%B %d, %Y – %I:%M:%S %p")
        earthquakes.append({
            'magnitude': mag,
            'place': place,
            'time': time,
            'warning': mag is not None and mag >= 5
        })

    return render_template('index.html', earthquakes=earthquakes)
    
if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)
