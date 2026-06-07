import os
import requests
from flask import Flask, render_template, redirect, url_for
from dotenv import load_dotenv
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger

import db
import led

load_dotenv()
db.init_db()

app = Flask(__name__)
FLOWER_URL = os.getenv('FLOWER_URL', 'http://192.168.0.29:5566')

def do_read():
    try:
        response = requests.get(f"{FLOWER_URL}/read", timeout=10)
        response.raise_for_status()
        data = response.json()
        db.save_reading(data['timestamp'], data['ettan'], data['spansk_timjan'], data['nummer_3'])
        led.notify_if_dry(data['ettan'], data['spansk_timjan'], data['nummer_3'])
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
