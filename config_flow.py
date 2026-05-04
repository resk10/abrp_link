from homeassistant import config_entries
import voluptuous as vol
from .const import DOMAIN

class ABRPLinkConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for ABRP Link."""
    
    VERSION = 1

    async def async_step_user(self, user_input=None):
        """Handle the initial step."""
        errors = {}
        
        if user_input is not None:
            # You could add validation here if you wanted
            return self.async_create_entry(title="BYD Seal ABRP Sync", data=user_input)

        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema({
                vol.Required("abrp_token"): str,
            }),
            errors=errors,
        )
