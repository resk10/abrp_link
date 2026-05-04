import logging
import json
import httpx
import time
import asyncio
from homeassistant.core import HomeAssistant
from homeassistant.helpers.event import async_track_state_change_event, async_track_time_interval
from datetime import timedelta
from .const import DOMAIN, ABRP_API_URL, ABRP_API_KEY

_LOGGER = logging.getLogger(__name__)

async def async_setup_entry(hass: HomeAssistant, entry):
    """Set up ABRP Link."""
    # Register the select entity
    await hass.config_entries.async_forward_entry_setups(entry, ["select"])
    
    token = entry.data.get("abrp_token")
    entities = ["sensor.byd_seal_battery_level", "device_tracker.byd_seal_location", "sensor.byd_seal_odometer"]

    async def _perform_sync():
        """The actual sync work."""
        # Get the current mode from our select entity
        mode_state = hass.states.get(f"select.abrp_sync_mode")
        mode = mode_state.state if mode_state else "Background (Default)"

        if mode == "Off":
            return

        soc_s = hass.states.get("sensor.byd_seal_battery_level")
        gps_s = hass.states.get("device_tracker.byd_seal_location")
        odo_s = hass.states.get("sensor.byd_seal_odometer")

        if not soc_s or not gps_s:
            return

        try:
            payload = {
                "utc": int(time.time()),
                "soc": float(soc_s.state),
                "lat": gps_s.attributes.get("latitude"),
                "lon": gps_s.attributes.get("longitude"),
                "odometer": float(odo_s.state.replace(",", "")) if odo_s else None,
                "is_charging": hass.states.is_state("binary_sensor.byd_seal_charging", "on")
            }

            params = {"api_key": ABRP_API_KEY, "token": token, "tlm": json.dumps(payload)}
            async with httpx.AsyncClient(verify=False) as client:
                await client.post(ABRP_API_URL, params=params)
                _LOGGER.info("ABRP Link (%s): Synced %s%%", mode, payload["soc"])
        except Exception as err:
            _LOGGER.error("Sync Error: %s", err)

    # MODE 1: Background (State Triggered)
    async def _on_state_change(event):
        mode_state = hass.states.get(f"select.abrp_sync_mode")
        if mode_state and mode_state.state == "Background (Default)":
            await _perform_sync()

    entry.async_on_unload(async_track_state_change_event(hass, entities, _on_state_change))

    # MODE 2: Force Always (Timer Triggered - Every 1 minute)
    async def _on_timer(now):
        mode_state = hass.states.get(f"select.abrp_sync_mode")
        if mode_state and mode_state.state == "Force Always":
            await _perform_sync()

    entry.async_on_unload(async_track_time_interval(hass, _on_timer, timedelta(minutes=1)))

    return True
