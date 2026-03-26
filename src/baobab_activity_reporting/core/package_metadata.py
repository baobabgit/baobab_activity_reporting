"""Module contenant les métadonnées du package."""

from importlib.metadata import PackageNotFoundError, version

from baobab_activity_reporting.exceptions.configuration_exception import (
    ConfigurationException,
)

_PACKAGE_NAME = "baobab-activity-reporting"


class PackageMetadata:
    """Fournit les métadonnées du package baobab-activity-reporting.

    Centralise l'accès au nom et à la version du package
    tels que définis dans ``pyproject.toml``.

    :ivar name: Nom du package.
    :vartype name: str
    :ivar package_version: Version sémantique du package.
    :vartype package_version: str

    :Example:
        >>> meta = PackageMetadata()
        >>> print(meta.name)
        baobab-activity-reporting
    """

    def __init__(self) -> None:
        """Initialise les métadonnées en lisant le package installé.

        :raises ConfigurationException: Si le package n'est pas installé.
        """
        self.name: str = _PACKAGE_NAME
        try:
            self.package_version: str = version(_PACKAGE_NAME)
        except PackageNotFoundError:
            raise ConfigurationException(
                "Package non installé",
                parameter_name=_PACKAGE_NAME,
                details="Exécutez 'pip install -e .[dev]'",
            ) from None

    def __repr__(self) -> str:
        """Retourne une représentation technique de l'objet.

        :return: Représentation incluant le nom et la version.
        :rtype: str
        """
        return f"PackageMetadata(name={self.name!r}, " f"package_version={self.package_version!r})"

    def summary(self) -> str:
        """Retourne un résumé lisible des métadonnées.

        :return: Chaîne au format ``nom vX.Y.Z``.
        :rtype: str
        """
        return f"{self.name} v{self.package_version}"
