"""Module contenant l'exception de standardisation."""

from baobab_activity_reporting.exceptions.reporting_error import (
    ReportingError,
)


class StandardizationError(ReportingError):
    """Exception levée lors d'une erreur de standardisation de données.

    Hérite de :class:`ReportingError` et représente les erreurs
    survenant lors du nettoyage, de la normalisation ou de
    l'harmonisation des données (conversion de type impossible,
    format de date invalide, etc.).

    :param message: Message décrivant l'erreur de standardisation.
    :type message: str
    :param column_name: Nom de la colonne en cause.
    :type column_name: str | None
    :param details: Détails complémentaires sur l'erreur.
    :type details: str | None

    :Example:
        >>> raise StandardizationError(
        ...     "Conversion de date impossible",
        ...     column_name="date_appel",
        ... )
    """

    def __init__(
        self,
        message: str,
        column_name: str | None = None,
        details: str | None = None,
    ) -> None:
        """Initialise l'exception de standardisation.

        :param message: Message décrivant l'erreur.
        :type message: str
        :param column_name: Nom de la colonne en cause.
        :type column_name: str | None
        :param details: Détails complémentaires.
        :type details: str | None
        """
        self.column_name: str | None = column_name
        if column_name is not None and details is None:
            details = f"colonne: {column_name}"
        elif column_name is not None and details is not None:
            details = f"colonne: {column_name}, {details}"
        super().__init__(message=message, details=details)
