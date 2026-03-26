"""Sous-package des exceptions du projet.

Regroupe la hiérarchie d'exceptions applicatives.
"""

from baobab_activity_reporting.exceptions.application_exception import (
    ApplicationException,
)
from baobab_activity_reporting.exceptions.configuration_exception import (
    ConfigurationException,
)

__all__: list[str] = [
    "ApplicationException",
    "ConfigurationException",
]
