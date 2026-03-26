"""Module contenant l'exception de configuration du projet."""

from baobab_activity_reporting.exceptions.application_exception import (
    ApplicationException,
)


class ConfigurationException(ApplicationException):
    """Exception levée lors d'une erreur de configuration.

    Hérite de :class:`ApplicationException` et représente les erreurs
    liées à la configuration de l'application (paramètres manquants,
    valeurs invalides, fichiers de configuration absents, etc.).

    :param message: Message décrivant l'erreur de configuration.
    :type message: str
    :param parameter_name: Nom du paramètre de configuration en cause.
    :type parameter_name: str | None
    :param details: Détails complémentaires sur l'erreur.
    :type details: str | None

    :Example:
        >>> raise ConfigurationException(
        ...     "Paramètre manquant",
        ...     parameter_name="database_url",
        ... )
    """

    def __init__(
        self,
        message: str,
        parameter_name: str | None = None,
        details: str | None = None,
    ) -> None:
        """Initialise l'exception de configuration.

        :param message: Message décrivant l'erreur de configuration.
        :type message: str
        :param parameter_name: Nom du paramètre en cause.
        :type parameter_name: str | None
        :param details: Détails complémentaires sur l'erreur.
        :type details: str | None
        """
        self.parameter_name: str | None = parameter_name
        if parameter_name is not None and details is None:
            details = f"paramètre: {parameter_name}"
        elif parameter_name is not None and details is not None:
            details = f"paramètre: {parameter_name}, {details}"
        super().__init__(message=message, details=details)

    def __repr__(self) -> str:
        """Retourne une représentation technique de l'exception.

        :return: Représentation technique incluant la classe et les attributs.
        :rtype: str
        """
        class_name = type(self).__name__
        return (
            f"{class_name}("
            f"message={self.message!r}, "
            f"parameter_name={self.parameter_name!r}, "
            f"details={self.details!r})"
        )
