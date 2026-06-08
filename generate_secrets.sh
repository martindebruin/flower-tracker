#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"

if [ ! -f config.env ]; then
  echo "config.env not found. Copy config.env.example and fill in your values."
  exit 1
fi

source config.env

cat > esp32-sensor/secrets.yaml <<EOF
wifi_ssid: "${WIFI_SSID}"
wifi_password: "${WIFI_PASSWORD}"
api_encryption_key: "${ESP32_API_KEY}"
ota_password: "${ESP32_OTA_PASSWORD}"
EOF

echo "esp32-sensor/secrets.yaml generated."
