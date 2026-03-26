"""Module contenant l'exception générale de reporting."""

from baobab_activity_reporting.exceptions.application_exception import (
    ApplicationException,
)


class ReportingError(ApplicationException):
    """Exception générale liée au domaine du reporting.

    Sert de classe parente pour toutes les exceptions métier
    spécifiques au pipeline de reporting. Hérite de
    :class:`ApplicationException`.

    :param message: Message décrivant l'erreur de reporting.
    :type message: str
    :param details: Détails complémentaires sur l'erreur.
    :type details: str | None

    :Example:
        >>> raise ReportingError("Erreur dans le pipeline de reporting")
    """

    def __init__(
        self,
        message: str,
        details: str | None = None,
    ) -> None:
        """Initialise l'exception de reporting.

        :param message: Message décrivant l'erreur.
        :type message: str
        :param details: Détails complémentaires.
        :type details: str | None
        """
        super().__init__(message=message, details=details)
