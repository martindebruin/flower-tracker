import time
import requests
from RPLCD.i2c import CharLCD

ESP32_HOST = "ESP32_SENSOR_HOST"
POLL_INTERVAL = 2 * 60 * 60  # 2 hours
DISPLAY_INTERVAL = 3

PLANTS = [
    ("TRADESCANTIA", "tradescantia_pallida"),
    ("AFRICAN MILK", "african_milk_bush"),
    ("SPANSK TIMJAN", "spansk_timjan"),
    ("PALETTBLADEN", "palettbladen"),
]

def fetch_readings():
    results = {}
    for name, sensor_id in PLANTS:
        try:
            r = requests.get(f"http://{ESP32_HOST}/binary_sensor/{sensor_id}", timeout=5)
            results[name] = "FUKTIG" if r.json()["value"] else "TORR"
        except Exception:
            results[name] = "FEL"
    return results

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
