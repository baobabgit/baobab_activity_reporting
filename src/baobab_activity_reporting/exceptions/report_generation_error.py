"""Module contenant l'exception de génération de rapport."""

from baobab_activity_reporting.exceptions.reporting_error import (
    ReportingError,
)


class ReportGenerationError(ReportingError):
    """Exception levée lors d'une erreur de génération de rapport.

    Hérite de :class:`ReportingError` et représente les erreurs
    survenant lors de la planification, de la construction ou de
    l'assemblage du rapport (données insuffisantes, section
    non constructible, etc.).

    :param message: Message décrivant l'erreur de génération.
    :type message: str
    :param report_type: Type de rapport concerné.
    :type report_type: str | None
    :param details: Détails complémentaires sur l'erreur.
    :type details: str | None

    :Example:
        >>> raise ReportGenerationError(
        ...     "Données insuffisantes pour le rapport",
        ...     report_type="activité_téléphonique",
        ... )
    """

    def __init__(
        self,
        message: str,
        report_type: str | None = None,
        details: str | None = None,
    ) -> None:
        """Initialise l'exception de génération de rapport.

        :param message: Message décrivant l'erreur.
        :type message: str
        :param report_type: Type de rapport en cause.
        :type report_type: str | None
        :param details: Détails complémentaires.
        :type details: str | None
        """
        self.report_type: str | None = report_type
        if report_type is not None and details is None:
            details = f"rapport: {report_type}"
        elif report_type is not None and details is not None:
            details = f"rapport: {report_type}, {details}"
        super().__init__(message=message, details=details)
