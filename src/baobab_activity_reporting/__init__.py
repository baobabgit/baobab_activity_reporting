"""Package racine de baobab_activity_reporting.

Ce package fournit l'ossature du projet de reporting d'activité Baobab.
"""

from baobab_activity_reporting.core.package_metadata import PackageMetadata
from baobab_activity_reporting.exceptions.application_exception import (
    ApplicationException,
)
from baobab_activity_reporting.exceptions.configuration_exception import (
    ConfigurationException,
)

__all__: list[str] = [
    "ApplicationException",
    "ConfigurationException",
    "PackageMetadata",
]
