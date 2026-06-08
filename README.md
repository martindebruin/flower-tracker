# Lilla Essingen Flower Tracker

Soil moisture monitoring for houseplants. Reads 4 sensors, shows status on a web UI, LED matrix, and local LCD display.

## Architecture

```
ESP32-C6                          RPi (web server)
├── 4× moisture sensors      →    flower-app (Flask)
│   via DO pins + ESPHome         ├── polls ESP32 every 2h
│   binary_sensor REST API        ├── SQLite storage
│                                 ├── Web UI (Tailscale)
│                                 └── LED matrix alerts

RPi Zero 2 W H (sensor display)
└── 1602 I2C LCD
    cycles through plants every 3s, refreshes data every 2h
```

## Plants

| Plant | Sensor GPIO |
|-------|-------------|
| Tradescantia Pallida | GPIO0 |
| African Milk Bush | GPIO1 |
| Spansk Timjan | GPIO2 |
| Palettbladen | GPIO3 |

## Hardware

- ESP32-C6-DevKitC-1 — sensor node
- 4× AZ-Delivery MH-Sensor-Series resistive moisture sensors (DO pin)
- 2× Wago 221 5-pos — power distribution (brown = VCC/3.3V, white = GND)
- RPi Zero 2 W H — LCD display
- RPi — web app + LED matrix controller
- 1602 I2C LCD (GJD 1602IIC, address 0x3f) — local plant status display
- ESP32-C6 LED matrix — dry plant alerts

## Services

| Service | Description |
|---------|-------------|
| `flower-app.service` | Flask web app (RPi web server) |
| `flower-lcd.service` | LCD display loop (RPi display) |
| ESPHome | Sensor firmware + REST API (ESP32-C6) |

## Repo Structure

```
esp32-sensor/        ESPHome firmware config
flower-app/          Flask web app
lcd-display/         LCD display script
sensor-api/          Retired — was RPi GPIO sensor API
```

## Setup

Copy `config.env.example` to `config.env` and fill in your values. Generate ESPHome secrets:

```bash
./generate_secrets.sh
```

## Deployment

**ESP32 firmware:**
```bash
cd esp32-sensor
esphome run flower_sensor.yaml
```

**flower-app:**
```bash
rsync -av flower-app/db.py flower-app/app.py flower-app/led.py <web-rpi>:~/flower-app/
rsync -av flower-app/templates/index.html <web-rpi>:~/flower-app/templates/index.html
ssh <web-rpi> "sudo systemctl restart flower-app"
```

**LCD display:**
```bash
rsync -av lcd-display/lcd_display.py <display-rpi>:~/lcd-display/
ssh <display-rpi> "sudo systemctl restart flower-lcd"
```

## Adding a New Sensor

1. Wire DO pin → next free ESP32 GPIO
2. Add `binary_sensor` entry to `esp32-sensor/flower_sensor.yaml`
3. Flash: `esphome run flower_sensor.yaml`
4. Add plant column to `flower-app/db.py`, `app.py`, `led.py`, `templates/index.html`
5. Delete `~/flower-app/data/readings.db` on the web RPi
6. Redeploy flower-app
7. Add plant to `PLANTS` list in `lcd-display/lcd_display.py`
8. Redeploy LCD display
