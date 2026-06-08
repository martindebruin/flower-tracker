# Lilla Essingen Flower Tracker

Soil moisture monitoring for houseplants. Reads 4 sensors, shows status on a web UI, LED matrix, and local LCD display.

## Architecture

```
ESP32-C6                          rpi-ess-general
├── 4× moisture sensors      →    flower-app (Flask, port 5566)
│   via DO pins + ESPHome         ├── polls ESP32 every 2h
│   binary_sensor REST API        ├── SQLite storage
│                                 ├── Web UI (Tailscale)
│                                 └── LED matrix alerts

rpi-ess-flower (RPi Zero 2 W H)
└── 1602 I2C LCD
    cycles through plant status every 3s
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
- RPi Zero 2 W H (`rpi-ess-flower`) — LCD display
- RPi (`rpi-ess-general`) — web app + LED matrix controller
- 1602 I2C LCD (GJD 1602IIC, address 0x3f) — local plant status display
- ESP32-C6 LED matrix — dry plant alerts

## Services

| Service | Host | Description |
|---------|------|-------------|
| `flower-app.service` | rpi-ess-general | Flask web app |
| `flower-lcd.service` | rpi-ess-flower | LCD display loop |
| ESPHome | ESP32-C6 | Sensor firmware + REST API |

## Repo Structure

```
esp32-sensor/        ESPHome firmware config
flower-app/          Flask web app (rpi-ess-general)
lcd-display/         LCD display script (rpi-ess-flower)
sensor-api/          Retired — was RPi GPIO sensor API
```

## Deployment

**ESP32 firmware:**
```bash
cd esp32-sensor
esphome run flower_sensor.yaml
```

**flower-app:**
```bash
rsync -av flower-app/db.py flower-app/app.py flower-app/led.py martin@rpi-ess-general:~/flower-app/
rsync -av flower-app/templates/index.html martin@rpi-ess-general:~/flower-app/templates/index.html
ssh martin@rpi-ess-general "sudo systemctl restart flower-app"
```

**LCD display:**
```bash
rsync -av lcd-display/lcd_display.py martin@rpi-ess-flower:~/lcd-display/
ssh martin@rpi-ess-flower "sudo systemctl restart flower-lcd"
```

## Adding a New Sensor

1. Wire DO pin → next free ESP32 GPIO
2. Add `binary_sensor` entry to `esp32-sensor/flower_sensor.yaml`
3. Flash: `esphome run flower_sensor.yaml`
4. Add plant column to `flower-app/db.py`, `app.py`, `led.py`, `templates/index.html`
5. Delete `~/flower-app/data/readings.db` on rpi-ess-general
6. Redeploy flower-app
7. Add plant to `PLANTS` list in `lcd-display/lcd_display.py`
8. Redeploy LCD display
