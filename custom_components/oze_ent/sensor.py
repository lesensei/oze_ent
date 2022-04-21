"""Sensor platform for Oze ENT."""
from homeassistant.components.sensor import SensorEntity
from homeassistant.util import dt
from homeassistant.const import DEVICE_CLASS_TIMESTAMP

from .const import DEFAULT_NAME, DOMAIN, ICON
from .entity import OzeEntity


async def async_setup_entry(hass, entry, async_add_devices):
    """Setup sensor platform."""
    coordinator = hass.data[DOMAIN][entry.entry_id]
    user_info = coordinator.data.get("user_info")
    devices = []
    for pupil in coordinator.api.userinfo.get_pupils_from_userinfo(user_info):
        devices.append(HomeworkSensor(coordinator, entry, pupil))
        devices.append(EndOfClassesSensor(coordinator, entry, pupil))
    async_add_devices(devices)


class HomeworkSensor(OzeEntity, SensorEntity):
    """Oze Homework sensor returns the number of unchecked homework entries."""

    def __init__(self, coordinator, config_entry, pupil: dict[str, str]):
        super().__init__(coordinator, config_entry)
        self._pupil = pupil

    @property
    def unique_id(self):
        return f"{DEFAULT_NAME}_{self._pupil['uid']}_homework_todo"

    @property
    def name(self):
        """Return the name of the sensor."""
        return f"{DEFAULT_NAME}_{self._pupil['first_name']}_homework_todo"

    @property
    def native_value(self):
        """Return the native value of the sensor."""
        return self.coordinator.data.get(self._pupil["uid"]).get("homeworks").get(
            "nbTravailTotal"
        ) - self.coordinator.data.get(self._pupil["uid"]).get("homeworks").get(
            "nbTravailFait"
        )

    @property
    def icon(self):
        """Return the icon of the sensor."""
        return ICON

    @property
    def extra_state_attributes(self):
        """Return the device state attributes."""
        homeworks = []
        for hday in (
            self.coordinator.data.get(self._pupil["uid"])
            .get("homeworks")
            .get("listJours")
        ):
            for homework in hday.get("listTravail"):
                homeworks.append(
                    {
                        "discipline": homework["matiere"],
                        "type": homework["type"],
                        "due_date": hday["date"],
                        "done": homework["fait"],
                        "content": homework["description"],
                    }
                )
        return {
            "homeworks": homeworks,
            "completed": self.coordinator.data.get(self._pupil["uid"])
            .get("homeworks")
            .get("nbTravailFait"),
        }


class EndOfClassesSensor(OzeEntity, SensorEntity):
    """Oze End of Classes sensor returns the datetime of the end of the day's last class."""

    def __init__(self, coordinator, config_entry, pupil: dict[str, str]):
        super().__init__(coordinator, config_entry)
        self._pupil = pupil

    @property
    def unique_id(self):
        return f"{DEFAULT_NAME}_{self._pupil['uid']}_end_of_classes"

    @property
    def name(self):
        """Return the name of the sensor."""
        return f"{DEFAULT_NAME}_{self._pupil['first_name']}_end_of_classes"

    @property
    def device_class(self):
        """Return the class of this binary_sensor."""
        return DEVICE_CLASS_TIMESTAMP

    @property
    def native_value(self):
        """Return the native value of the sensor."""
        classes = self.coordinator.data.get(self._pupil["uid"]).get("classes")
        classes = list(
            filter(
                lambda cl: dt.parse_datetime(cl["dateFin"]).date() == dt.now().date(),
                classes,
            )
        )
        classes.sort(key=lambda cl: cl["dateFin"], reverse=True)

        return dt.parse_datetime(classes[0]["dateFin"])

    @property
    def icon(self):
        """Return the icon of the sensor."""
        return "mdi:clock-end"

    @property
    def extra_state_attributes(self):
        """Return the device state attributes."""
        classes = self.coordinator.data.get(self._pupil["uid"]).get("classes")
        classes.sort(key=lambda cl: cl["dateFin"], reverse=True)
        return {
            "class": classes[0],
        }
