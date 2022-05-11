"""OzeEntity class"""
from homeassistant.helpers.update_coordinator import CoordinatorEntity
from homeassistant.helpers.entity import DeviceInfo
from homeassistant.helpers.device_registry import DeviceEntryType

from .const import DOMAIN, NAME, VERSION, CONF_UID, DEFAULT_NAME, MANUFACTURER


class OzeEntity(CoordinatorEntity):
    """HA coordinator class for Oze integration"""

    def __init__(self, coordinator, config_entry):
        super().__init__(coordinator)
        self.config_entry = config_entry

    @property
    def unique_id(self):
        """Return a unique ID to use for this entity."""
        return f"{DEFAULT_NAME}_{self.config_entry.data.get(CONF_UID)}"

    @property
    def device_info(self):
        """Return information on 'device'"""
        return DeviceInfo(
            entry_type=DeviceEntryType.SERVICE,
            identifiers={(DOMAIN, self.unique_id)},
            manufacturer=MANUFACTURER,
            model=NAME,
            name=NAME,
        )

    @property
    def extra_state_attributes(self):
        """Return the state attributes."""
        return {
            "id": self.config_entry.data.get(CONF_UID),
            "integration": DOMAIN,
        }
