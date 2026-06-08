import os
import datetime
import requests
from flask import Flask, render_template, redirect, url_for
from dotenv import load_dotenv
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger

import db
import led

load_dotenv(os.path.join(os.path.dirname(__file__), '..', 'config.env'))
db.init_db()

app = Flask(__name__)
ESP32_SENSOR_HOST = os.getenv('ESP32_SENSOR_HOST')

def read_sensor(sensor_id):
    response = requests.get(f"http://{ESP32_SENSOR_HOST}/binary_sensor/{sensor_id}", timeout=10)
    response.raise_for_status()
    return "wet" if response.json()['value'] else "dry"

def do_read():
    try:
        tradescantia = read_sensor('tradescantia_pallida')
        african_milk_bush = read_sensor('african_milk_bush')
        spansk_timjan = read_sensor('spansk_timjan')
        palettbladen = read_sensor('palettbladen')
        timestamp = datetime.datetime.now().isoformat()
        db.save_reading(timestamp, tradescantia, african_milk_bush, spansk_timjan, palettbladen)
        led.notify_if_dry(tradescantia, african_milk_bush, spansk_timjan, palettbladen)
    except Exception as e:
        print(f"Error in do_read: {e}")

scheduler = BackgroundScheduler()
scheduler.add_job(
    func=do_read,
    trigger=IntervalTrigger(hours=2),
    id='flower_reading_job',
    name='Read flower sensor data every 2 hours',
    replace_existing=True
)

@app.route('/', methods=['GET'])
def index():
    reading = db.get_latest()
    return render_template('index.html', reading=reading)

@app.route('/read-now', methods=['POST'])
def read_now():
    do_read()
    return redirect(url_for('index'))

if __name__ == '__main__':
    scheduler.start()
    app.run(host='0.0.0.0', port=int(os.getenv('PORT', 5000)))
