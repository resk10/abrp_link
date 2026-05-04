# ABRP Link for BYD Seal (and other models, as long as they are supported by pyBYD, in which case you need to adjusst the Entity names)

A standalone Home Assistant integration that bridges your BYD Seal's telemetry (SOC, GPS, Odometer) to **A Better Routeplanner (ABRP)**.

## Why this exists?
This integration provides the ABRP sync logic from the main BYD vehicle integration. This ensures your sync stays active even if the main vehicle integration is updated or changed, as it relies on standard Home Assistant entities.

## Features
- **3-Way Sync Control:**
  - `Background`: Updates only when the car sends new data (saves battery/data).
  - `Force Always`: Syncs every 60 seconds regardless of state changes.
  - `Off`: Completely stops all communication with ABRP.
- **Native HA Integration:** Configured via the UI (Config Flow).
- **Lightweight:** Uses state-change listeners to minimize CPU usage.

## Installation

### Method 1: HACS (Recommended)
1. Open HACS in Home Assistant.
2. Click the three dots in the top right and select **Custom repositories**.
3. Paste the URL of this GitHub repository and select **Integration** as the category.
4. Click **Install**.
5. Restart Home Assistant.

### Method 2: Manual
1. Copy the `abrp_link` folder from `custom_components/` into your own `config/custom_components/` directory.
2. Restart Home Assistant.

## Setup
1. Go to **Settings > Devices & Services**.
2. Click **Add Integration** and search for **ABRP Link for BYD**.
3. Enter your **ABRP User Token** (found in ABRP Settings > Telemetry > Generic Graphana/JSON).

## Required Entities
This integration expects the following entities to exist (provided by the `byd_vehicle` integration):
- `sensor.byd_seal_battery_level`
- `sensor.byd_seal_odometer`
- `device_tracker.byd_seal_location`

## Debugging
To see sync confirmations in your logs, add this to your `configuration.yaml`:
```yaml
logger:
  default: info
  logs:
    custom_components.abrp_link: debug