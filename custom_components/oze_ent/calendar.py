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
        devices.append(ClassesCalendarEntity(coordinator, pupil))
        devices.append(PunishmentCalendarEntity(coordinator, pupil))
    async_add_devices(devices)


class ClassesCalendarEntity(CalendarEntity):
    """Oze classes calendar."""

    def __init__(self, oze: OzeEntity, pupil: dict[str, str]):
        """Create the Calendar Entity."""
        self.oze = oze
        self._event: CalendarEvent | None = None
        self._pupil = pupil
        self._attr_unique_id = f"{DEFAULT_NAME}_{self._pupil['uid']}_classes"

    @property
    def name(self):
        """Return a descriptive name for this sensor"""
        return f"{self._pupil['first_name']} classes"

    @property
    def event(self):
        """Return the next upcoming class event."""
        return self._event

    async def async_get_events(self, hass, start_date, end_date) -> list[CalendarEvent]:
        """Get all classes in a specific time frame."""
        events: list[dict[str, Any]] = await self.oze.api.event.get_events(
            pupil=self._pupil, start_date=start_date, end_date=end_date
        )
        event_list: list[CalendarEvent] = []
        for event in events:
            if event["_deletedStatus"] == 0:
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
        self._event = _get_calendar_event(events[0]) if len(events) > 0 else None


class PunishmentCalendarEntity(CalendarEntity):
    """Oze punishment calendar."""

    def __init__(self, oze: OzeEntity, pupil: dict[str, str]):
        """Create the Calendar Entity."""
        self.oze = oze
        self._event: CalendarEvent | None = None
        self._pupil = pupil
        self._attr_unique_id = f"{DEFAULT_NAME}_{self._pupil['uid']}_punishments"

    @property
    def name(self):
        """Return a descriptive name for this sensor"""
        return f"{self._pupil['first_name']} punishments"

    @property
    def event(self):
        """Return the next upcoming punishment event."""
        return self._event

    async def async_get_events(self, hass, start_date, end_date) -> list[CalendarEvent]:
        """Get all classes in a specific time frame."""
        punishments = await self.oze.api.punishment.get_punishments(
            pupil=self._pupil, start_date=start_date, end_date=end_date
        )
        event_list: list[CalendarEvent] = []
        for punishment in punishments:
            if punishment["typePunition"]["needPeriode"]:
                event_list.append(_get_calendar_event(punishment, True))
        return event_list

    def update(self):
        """Update current event."""
        events = self.oze.data.get(self._pupil["uid"]).get("punishments")
        nowtime = datetime.now(tz.gettz("Europe/Paris"))
        events = list(
            filter(lambda event: nowtime <= parser.parse(event["dateFin"]), events)
        )
        events.sort(key=lambda event: event["dateDebut"])
        self._event = _get_calendar_event(events[0], True) if len(events) > 0 else None


def _get_calendar_event(
    event: dict[str, Any], is_punishment: bool = False
) -> CalendarEvent:
    """Return a HA CalendarEvent from an Oze class or punishment"""
    prof = event["profs"][0] if not is_punishment else event["responsableSuivi"]
    return CalendarEvent(
        summary=event["matieres"][0]["libelle"]
        if not is_punishment
        else event["typePunition"]["libelle"],
        start=dt.parse_datetime(event["dateDebut"]),
        end=dt.parse_datetime(event["dateFin"]),
        description=prof["nom"] + " " + prof["prenom"],
        location=event["salles"][0]["libelle"]
        if "salles" in event and event["salles"]
        else "",
    )
