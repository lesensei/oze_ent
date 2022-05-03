# oze_ent

[![GitHub Release][releases-shield]][releases]
[![GitHub Activity][commits-shield]][commits]
[![License][license-shield]](LICENSE)

[![hacs][hacsbadge]][hacs]

[![Community Forum][forum-shield]][forum]

_Component to integrate with an oZe ENT using [aioZe][aioze]._

**This component will set up the following platforms.**

Platform | Description
-- | --
`sensor` | Show info from the ENT (homework info, last class end time for current day, ...).
`calendar` | Calendar entity for classes and punishments.

![example][exampleimg]

## Installation

1. Using the tool of choice open the directory (folder) for your HA configuration (where you find `configuration.yaml`).
2. If you do not have a `custom_components` directory (folder) there, you need to create it.
3. In the `custom_components` directory (folder) create a new folder called `integration_blueprint`.
4. Download _all_ the files from the `custom_components/integration_blueprint/` directory (folder) in this repository.
5. Place the files you downloaded in the new directory (folder) you created.
6. Restart Home Assistant
7. In the HA UI go to "Configuration" -> "Integrations" click "+" and search for "Integration blueprint"

Using your HA configuration directory (folder) as a starting point you should now also have this:

```text
custom_components/integration_blueprint/translations/en.json
custom_components/integration_blueprint/translations/nb.json
custom_components/integration_blueprint/translations/sensor.nb.json
custom_components/integration_blueprint/__init__.py
custom_components/integration_blueprint/api.py
custom_components/integration_blueprint/binary_sensor.py
custom_components/integration_blueprint/config_flow.py
custom_components/integration_blueprint/const.py
custom_components/integration_blueprint/manifest.json
custom_components/integration_blueprint/sensor.py
custom_components/integration_blueprint/switch.py
```

## Configuration is done in the UI

<!---->

## Contributions are welcome!

If you want to contribute to this please read the [Contribution guidelines](CONTRIBUTING.md)

***

[integration_blueprint]: https://github.com/lesensei/aioze
[commits-shield]: https://img.shields.io/github/commit-activity/y/lesensei/oze_ent.svg?style=for-the-badge
[commits]: https://github.com/lesensei/oze_ent/commits/master
[hacs]: https://github.com/custom-components/hacs
[hacsbadge]: https://img.shields.io/badge/HACS-Custom-orange.svg?style=for-the-badge
[exampleimg]: example.png
[forum-shield]: https://img.shields.io/badge/community-forum-brightgreen.svg?style=for-the-badge
[forum]: https://community.home-assistant.io/
[license-shield]: https://img.shields.io/github/license/lesensei/oze_ent.svg?style=for-the-badge
[releases-shield]: https://img.shields.io/github/release/lesensei/oze_ent.svg?style=for-the-badge
[releases]: https://github.com/lesensei/oze_ent/releases
[aioze]: https://github.com/lesensei/aioze