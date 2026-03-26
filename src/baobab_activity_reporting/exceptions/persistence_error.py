"""Module contenant l'exception de persistance."""

from baobab_activity_reporting.exceptions.reporting_error import (
    ReportingError,
)


class PersistenceError(ReportingError):
    """Exception levée lors d'une erreur de persistance.

    Hérite de :class:`ReportingError` et représente les erreurs
    survenant lors des opérations de lecture ou d'écriture en
    base de données (connexion échouée, requête invalide,
    contrainte violée, etc.).

    :param message: Message décrivant l'erreur de persistance.
    :type message: str
    :param operation: Nom de l'opération en cause (ex: ``insert``, ``select``).
    :type operation: str | None
    :param details: Détails complémentaires sur l'erreur.
    :type details: str | None

    :Example:
        >>> raise PersistenceError(
        ...     "Écriture impossible",
        ...     operation="insert",
        ... )
    """

    def __init__(
        self,
        message: str,
        operation: str | None = None,
        details: str | None = None,
    ) -> None:
        """Initialise l'exception de persistance.

        :param message: Message décrivant l'erreur.
        :type message: str
        :param operation: Opération en cause.
        :type operation: str | None
        :param details: Détails complémentaires.
        :type details: str | None
        """
        self.operation: str | None = operation
        if operation is not None and details is None:
            details = f"opération: {operation}"
        elif operation is not None and details is not None:
            details = f"opération: {operation}, {details}"
        super().__init__(message=message, details=details)
