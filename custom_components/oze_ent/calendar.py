"""Calendar platform for Oze ENT."""
from datetime import datetime
from typing import Any
from dateutil import parser, tz
from homeassistant.components.calendar import (
    CalendarEntity,
    CalendarEvent,
)
from homeassistant.util import dt

from .const import DOMAIN, DEFAULT_NAME
from .entity import OzeEntity


async def async_setup_entry(hass, entry, async_add_devices):
    """Setup sensor platform."""
    coordinator = hass.data[DOMAIN][entry.entry_id]
    user_info = coordinator.data.get("user_info")
    devices = []
    for pupil in coordinator.api.userinfo.get_pupils_from_userinfo(user_info):
        devices.append(OzeCalendarEntity(coordinator, pupil))
    async_add_devices(devices)


class OzeCalendarEntity(CalendarEntity):
    """Oze Calendar entity."""

    def __init__(self, oze: OzeEntity, pupil: dict[str, str]):
        """Create the Oze Calendar Entity."""
        self.oze = oze
        self._event: CalendarEvent | None = None
        self._pupil = pupil

    @property
    def unique_id(self) -> str | None:
        return f"{DEFAULT_NAME}_{self._pupil['uid']}_{DOMAIN}"

    @property
    def name(self) -> str | None:
        return f"{DEFAULT_NAME}_{self._pupil['first_name']}_{DOMAIN}"

    @property
    def event(self) -> CalendarEvent | None:
        """Return the next upcoming class event."""
        return self._event

    async def async_get_events(self, hass, start_date, end_date) -> list[CalendarEvent]:
        """Get all classes in a specific time frame."""
        events: list[dict[str, Any]] = await self.oze.api.event.get_events(
            pupil=self._pupil, start_date=start_date, end_date=end_date
        )
        event_list: list[CalendarEvent] = []
        for event in events:
            event_list.append(_get_calendar_event(event))
        return event_list

    def update(self):
        """Update current event."""
        events = self.oze.data.get(self._pupil["uid"]).get("classes")
        nowtime = datetime.now(tz.gettz("Europe/Paris"))
        events = list(
            filter(lambda event: nowtime <= parser.parse(event["dateFin"]), events)
        )
        events.sort(key=lambda event: event["dateDebut"])
        self._event = _get_calendar_event(events[0])


def _get_calendar_event(event: dict[str, Any]) -> CalendarEvent:
    """Return a HA CalendarEvent from an Oze event"""
    return CalendarEvent(
        summary=event["matieres"][0]["libelle"],
        start=dt.parse_datetime(event["dateDebut"]),
        end=dt.parse_datetime(event["dateFin"]),
        description=event["profs"][0]["nom"] + " " + event["profs"][0]["prenom"],
        location=event["salles"][0]["libelle"]
        if "salles" in event and event["salles"]
        else "",
    )
