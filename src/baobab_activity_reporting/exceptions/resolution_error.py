"""Module contenant l'exception de résolution métier."""

from baobab_activity_reporting.exceptions.reporting_error import (
    ReportingError,
)


class ResolutionError(ReportingError):
    """Exception levée lors d'une erreur de résolution métier.

    Hérite de :class:`ReportingError` et représente les erreurs
    survenant lors du rapprochement ou de la résolution de données
    entre jeux de données (agent non trouvé, site ambigu,
    rapprochement impossible, etc.).

    :param message: Message décrivant l'erreur de résolution.
    :type message: str
    :param entity_type: Type d'entité concernée par l'échec.
    :type entity_type: str | None
    :param details: Détails complémentaires sur l'erreur.
    :type details: str | None

    :Example:
        >>> raise ResolutionError(
        ...     "Agent non trouvé",
        ...     entity_type="Agent",
        ... )
    """

    def __init__(
        self,
        message: str,
        entity_type: str | None = None,
        details: str | None = None,
    ) -> None:
        """Initialise l'exception de résolution.

        :param message: Message décrivant l'erreur.
        :type message: str
        :param entity_type: Type d'entité en cause.
        :type entity_type: str | None
        :param details: Détails complémentaires.
        :type details: str | None
        """
        self.entity_type: str | None = entity_type
        if entity_type is not None and details is None:
            details = f"entité: {entity_type}"
        elif entity_type is not None and details is not None:
            details = f"entité: {entity_type}, {details}"
        super().__init__(message=message, details=details)
