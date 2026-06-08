import time
import requests
from RPLCD.i2c import CharLCD

ESP32_HOST = "ESP32_SENSOR_HOST"

PLANTS = [
    ("TRADESCANTIA", "tradescantia_pallida"),
    ("AFRICAN MILK", "african_milk_bush"),
    ("SPANSK TIMJAN", "spansk_timjan"),
    ("PALETTBLADEN", "palettbladen"),
]

def read_sensor(sensor_id):
    try:
        r = requests.get(f"http://{ESP32_HOST}/binary_sensor/{sensor_id}", timeout=5)
        return "FUKTIG" if r.json()["value"] else "TORR"
    except Exception:
        return "FEL"

def main():
    lcd = CharLCD(i2c_expander='PCF8574', address=0x3f, port=1,
                  cols=16, rows=2, charmap='A00',
                  auto_linebreaks=False)
    lcd.clear()
    lcd.write_string("FLOWER TRACKER")
    lcd.cursor_pos = (1, 0)
    lcd.write_string("Startar...")
    time.sleep(2)

    while True:
        for name, sensor_id in PLANTS:
            status = read_sensor(sensor_id)
            lcd.clear()
            lcd.write_string(name[:16].ljust(16))
            lcd.cursor_pos = (1, 0)
            lcd.write_string(status.ljust(16))
            time.sleep(3)

if __name__ == "__main__":
    main()
