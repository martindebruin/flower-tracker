import os
import time
import requests
from dotenv import load_dotenv
from RPLCD.i2c import CharLCD

load_dotenv(os.path.join(os.path.dirname(__file__), '..', 'config.env'))
SENSOR_API_HOST = os.getenv('SENSOR_API_HOST', 'localhost:5566')
POLL_INTERVAL = 2 * 60 * 60  # 2 hours
DISPLAY_INTERVAL = 3

PLANTS = [
    ("TRADESCANTIA", "tradescantia"),
    ("AFRICAN MILK", "african_milk_bush"),
    ("SPANSK TIMJAN", "spansk_timjan"),
]

def fetch_readings():
    try:
        r = requests.get(f"http://{SENSOR_API_HOST}/read", timeout=5)
        data = r.json()
        return {name: ("FUKTIG" if data.get(key) == "wet" else "TORR") for name, key in PLANTS}
    except Exception:
        return {name: "FEL" for name, _ in PLANTS}

def main():
    lcd = CharLCD(i2c_expander='PCF8574', address=0x3f, port=1,
                  cols=16, rows=2, charmap='A00',
                  auto_linebreaks=False)
    lcd.clear()
    lcd.write_string("FLOWER TRACKER")
    lcd.cursor_pos = (1, 0)
    lcd.write_string("Startar...")
    time.sleep(2)

    readings = fetch_readings()
    last_poll = time.time()

    while True:
        if time.time() - last_poll >= POLL_INTERVAL:
            readings = fetch_readings()
            last_poll = time.time()

        for name, _ in PLANTS:
            status = readings.get(name, "FEL")
            lcd.clear()
            lcd.write_string(name[:16].ljust(16))
            lcd.cursor_pos = (1, 0)
            lcd.write_string(status.ljust(16))
            time.sleep(DISPLAY_INTERVAL)

if __name__ == "__main__":
    main()
