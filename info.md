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

{% if not installed %}
## Installation

1. Click install.
1. In the HA UI go to "Configuration" -> "Integrations" click "+" and search for "OzE ENT".
1. Enter the URL and credentials you use to access your ENT.

{% endif %}


## Configuration is done in the UI

<!---->

***

[integration_blueprint]: https://github.com/custom-components/integration_blueprint
[commits-shield]: https://img.shields.io/github/commit-activity/y/lesensei/oze_ent.svg?style=for-the-badge
[commits]: https://github.com/lesensei/oze_ent/commits/master
[hacs]: https://hacs.xyz
[hacsbadge]: https://img.shields.io/badge/HACS-Custom-orange.svg?style=for-the-badge
[forum-shield]: https://img.shields.io/badge/community-forum-brightgreen.svg?style=for-the-badge
[forum]: https://forum.hacf.fr/t/integration-oze-ent-environnement-numerique-de-travail-2nd-degre/7277/
[license]: https://github.com/lesensei/oze_ent/blob/main/LICENSE
[license-shield]: https://img.shields.io/github/license/lesensei/oze_ent.svg?style=for-the-badge
[maintenance-shield]: https://img.shields.io/badge/maintainer-lesensei-blue.svg?style=for-the-badge
[releases-shield]: https://img.shields.io/github/release/lesensei/oze_ent.svg?style=for-the-badge
[releases]: https://github.com/lesensei/oze_ent/releases
[user_profile]: https://github.com/lesensei
[aioze]: https://github.com/lesensei/aioze
