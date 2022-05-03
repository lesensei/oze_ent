"""Constants for oze_ent."""
# Base component constants
NAME = "oZe ENT"
DOMAIN = "oze_ent"
DOMAIN_DATA = f"{DOMAIN}_data"
VERSION = "0.0.1"
ISSUE_URL = "https://github.com/lesensei/oze_ent/issues"

# Icons
ICON = "mdi:school"

# Device classes
BINARY_SENSOR_DEVICE_CLASS = "presence"

# Platforms
BINARY_SENSOR = "binary_sensor"
CALENDAR = "calendar"
SENSOR = "sensor"
PLATFORMS = [CALENDAR, SENSOR]


# Configuration and options
CONF_ENABLED = "enabled"
CONF_URL = "url"
CONF_USERNAME = "username"
CONF_PASSWORD = "password"

# Defaults
DEFAULT_NAME = "oze"


STARTUP_MESSAGE = f"""
-------------------------------------------------------------------
{NAME}
Version: {VERSION}
This is a custom integration!
If you have any issues with this you need to open an issue here:
{ISSUE_URL}
-------------------------------------------------------------------
"""
