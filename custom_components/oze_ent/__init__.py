"""
Custom integration to integrate an oZe ENT with Home Assistant.

For more details about this integration, please refer to
https://github.com/lesensei/oze_ent
"""
import asyncio
from datetime import datetime, timedelta
import logging

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import Config, HomeAssistant
from homeassistant.exceptions import ConfigEntryNotReady
from homeassistant.helpers.aiohttp_client import async_get_clientsession
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

from aioze import OzeApiClient

from .const import (
    CONF_URL,
    CONF_PASSWORD,
    CONF_USERNAME,
    DOMAIN,
    PLATFORMS,
    STARTUP_MESSAGE,
)

SCAN_INTERVAL = timedelta(seconds=300)

_LOGGER: logging.Logger = logging.getLogger(__package__)


async def async_setup(hass: HomeAssistant, config: Config):
    """Set up this integration using YAML is not supported."""
    return True


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry):
    """Set up this integration using UI."""
    if hass.data.get(DOMAIN) is None:
        hass.data.setdefault(DOMAIN, {})
        _LOGGER.info(STARTUP_MESSAGE)

    url = entry.data.get(CONF_URL)
    username = entry.data.get(CONF_USERNAME)
    password = entry.data.get(CONF_PASSWORD)

    session = async_get_clientsession(hass)
    client = OzeApiClient(url, username, password, session)
    await client.connect()

    coordinator = BlueprintDataUpdateCoordinator(hass, client=client)
    await coordinator.async_refresh()

    if not coordinator.last_update_success:
        raise ConfigEntryNotReady

    hass.data[DOMAIN][entry.entry_id] = coordinator

    for platform in PLATFORMS:
        if entry.options.get(platform, True):
            coordinator.platforms.append(platform)
            hass.async_add_job(
                hass.config_entries.async_forward_entry_setup(entry, platform)
            )

    entry.async_on_unload(entry.add_update_listener(async_reload_entry))
    return True


class BlueprintDataUpdateCoordinator(DataUpdateCoordinator):
    """Class to manage fetching data from the API."""

    def __init__(self, hass: HomeAssistant, client: OzeApiClient) -> None:
        """Initialize."""
        self.api = client
        self.platforms = []

        super().__init__(hass, _LOGGER, name=DOMAIN, update_interval=SCAN_INTERVAL)

    async def _async_update_data(self) -> dict:
        """Update data via library."""
        user_info = await self.api.userinfo.get_user_info()
        pupils = self.api.userinfo.get_pupils_from_userinfo(user_info)
        pupil_data = {}
        for pupil in pupils:
            pupil_data[pupil["uid"]] = {
                "homeworks": await self.api.homework.get_homework(pupil),
                "punishments": await self.api.punishment.get_punishments(
                    pupil=pupil, start_date=datetime.utcnow()
                ),
                "classes": await self.api.event.get_events(
                    pupil=pupil, start_date=datetime.utcnow()
                ),
            }
        try:
            return {
                "user_info": user_info,
                "notifications": await self.api.notification.get_notifications(
                    pupil=pupils[0]
                ),
                "notices": await self.api.information.get_informations(pupil=pupils[0]),
            } | pupil_data
        except Exception as exception:
            raise UpdateFailed() from exception


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Handle removal of an entry."""
    coordinator = hass.data[DOMAIN][entry.entry_id]
    unloaded = all(
        await asyncio.gather(
            *[
                hass.config_entries.async_forward_entry_unload(entry, platform)
                for platform in PLATFORMS
                if platform in coordinator.platforms
            ]
        )
    )
    if unloaded:
        hass.data[DOMAIN].pop(entry.entry_id)

    return unloaded


async def async_reload_entry(hass: HomeAssistant, entry: ConfigEntry) -> None:
    """Reload config entry."""
    await async_unload_entry(hass, entry)
    await async_setup_entry(hass, entry)
