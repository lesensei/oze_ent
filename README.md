# oze_ent

[![GitHub Release][releases-shield]][releases]
[![GitHub Activity][commits-shield]][commits]
[![License][license-shield]](LICENSE)

[![hacs][hacsbadge]][hacs]

[![Community Forum][forum-shield]][forum]

_Component to integrate with an OzE ENT using [aioZe][aioze]._

**This component will set up the following platforms.**

Platform | Description
-- | --
`sensor` | Shows remaining homework, unread emails, unread notifications, unread information notices, mean grade and time of end of classes for the current day.
`binary_sensor` | Set to '`on`' on days with classes.
`calendar` | One calendar for classes and another for punishment periods.

![example][exampleimg]

## Installation with HACS

1. Install [HACS][hacs]
2. Got to the HACS UI in HA, then "Integrations", use the 3 vertical dots menu and choose "Custom repositories"
3. Paste the URL to this repository and choose the "Integration" category".
4. Back on the "Integrations" page, click "explore and search" then add this integration.

## Installation

1. Using the tool of choice open the directory (folder) for your HA configuration (where you find `configuration.yaml`).
2. If you do not have a `custom_components` directory (folder) there, you need to create it.
3. In the `custom_components` directory (folder) create a new folder called `oze_ent`.
4. Download _all_ the files from the `custom_components/oze_ent/` directory (folder) in this repository.
5. Place the files you downloaded in the new directory (folder) you created.
6. Restart Home Assistant
7. In the HA UI go to "Configuration" -> "Integrations" click "+" and search for "Integration blueprint"

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