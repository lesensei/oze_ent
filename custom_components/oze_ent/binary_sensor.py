"""Binary sensor platform for oze_int."""
from dateutil import parser
from homeassistant.components.binary_sensor import BinarySensorEntity
from homeassistant.util import dt

from .const import (
    DEFAULT_NAME,
    DOMAIN,
)
from .entity import OzeEntity


async def async_setup_entry(hass, entry, async_add_devices):
    """Setup binary_sensor platform."""
    coordinator = hass.data[DOMAIN][entry.entry_id]
    user_info = coordinator.data.get("user_info")
    devices = []
    for pupil in coordinator.api.userinfo.get_pupils_from_userinfo(user_info):
        devices.append(ClassDayBinarySensor(coordinator, entry, pupil))
    async_add_devices(devices)


class ClassDayBinarySensor(OzeEntity, BinarySensorEntity):
    """Binary sensor that's on days with classes."""

    def __init__(self, coordinator, config_entry, pupil: dict[str, str]):
        super().__init__(coordinator, config_entry)
        self._pupil = pupil
        self._attr_unique_id = f"{DEFAULT_NAME}_{self._pupil['uid']}_class_day"
        self._attr_name = f"{self._pupil['first_name']} class day"

    @property
    def device_class(self):
        """Return the class of this binary_sensor."""
        return None

    @property
    def is_on(self):
        """Return true if a class is currently ongoing."""
        # now = datetime.now(tz.gettz("Europe/Paris"))
        events = self.coordinator.data.get(self._pupil["uid"]).get("classes")
        current_events = filter(
            lambda event: parser.parse(event["dateDebut"]).date() == dt.now().date(),
            events,
        )
        try:
            next(current_events)
            return True
        except StopIteration:
            return False
