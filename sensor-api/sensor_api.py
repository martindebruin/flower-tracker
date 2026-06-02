import os
import datetime
from flask import Flask, jsonify
from dotenv import load_dotenv

import RPi.GPIO as GPIO

# Setup GPIO at module level
GPIO.setmode(GPIO.BCM)
GPIO.setup(17, GPIO.IN)
GPIO.setup(22, GPIO.IN)

# Load environment variables
load_dotenv()
PORT = int(os.getenv("PORT", 5000))

app = Flask(__name__)

@app.route("/read", methods=["GET"])
def read_sensors():
    ettan = "wet" if GPIO.input(17) == 0 else "dry"
    spansk_timjan = "wet" if GPIO.input(22) == 0 else "dry"
    timestamp = datetime.datetime.now().isoformat()
    return jsonify({
        "ettan": ettan,
        "spansk_timjan": spansk_timjan,
        "timestamp": timestamp
    })

@app.route("/health", methods=["GET"])
def health_check():
    return jsonify({"ok": True})

import atexit
atexit.register(GPIO.cleanup)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=PORT)
