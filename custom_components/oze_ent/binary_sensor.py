"""Binary sensor platform for oze_int."""
from dateutil import parser
from homeassistant.components.binary_sensor import BinarySensorEntity
from homeassistant.util import dt

from .const import (
    BINARY_SENSOR_DEVICE_CLASS,
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
        devices.append(ClassInProgressBinarySensor(coordinator, entry, pupil))
    async_add_devices(devices)


class ClassInProgressBinarySensor(OzeEntity, BinarySensorEntity):
    """integration_blueprint binary_sensor class."""

    def __init__(self, coordinator, config_entry, pupil: dict[str, str]):
        super().__init__(coordinator, config_entry)
        self._pupil = pupil

    @property
    def unique_id(self):
        return f"{DEFAULT_NAME}_{self._pupil['uid']}_class_in_progress"

    @property
    def name(self):
        """Return the name of the sensor."""
        return f"{DEFAULT_NAME}_{self._pupil['uid']}_class_in_progress"

    @property
    def device_class(self):
        """Return the class of this binary_sensor."""
        return BINARY_SENSOR_DEVICE_CLASS

    @property
    def is_on(self):
        """Return true if a class is currently ongoing."""
        # now = datetime.now(tz.gettz("Europe/Paris"))
        events = self.coordinator.data.get(self._pupil["uid"]).get("classes")
        current_events = filter(
            lambda event: parser.parse(event["dateDebut"])
            <= dt.now()
            <= parser.parse(event["dateFin"]),
            events,
        )
        try:
            next(current_events)
            return True
        except StopIteration:
            return False
