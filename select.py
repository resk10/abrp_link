from homeassistant.components.select import SelectEntity
from .const import DOMAIN

async def async_setup_entry(hass, entry, async_add_entities):
    """Set up the ABRP Link select entity."""
    async_add_entities([ABRPSyncModeSelect(entry)])

class ABRPSyncModeSelect(SelectEntity):
    """Control the sync behavior of ABRP Link."""

    def __init__(self, entry):
        self._entry = entry
        self._attr_name = "ABRP Sync Mode"
        self._attr_unique_id = f"{entry.entry_id}_sync_mode"
        self._attr_options = ["Background (Default)", "Force Always", "Off"]
        self._attr_current_option = "Background (Default)"
        self._attr_icon = "mdi:sync-cog"

    async def async_select_option(self, option: str) -> None:
        """Update the current selected option."""
        self._attr_current_option = option
        self.async_write_ha_state()
