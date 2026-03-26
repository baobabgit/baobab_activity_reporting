"""Module contenant l'exception de validation."""

from baobab_activity_reporting.exceptions.reporting_error import (
    ReportingError,
)


class ValidationError(ReportingError):
    """Exception levée lors d'une erreur de validation de données.

    Hérite de :class:`ReportingError` et représente les erreurs
    survenant lors du contrôle de conformité des données (colonnes
    manquantes, types incorrects, valeurs hors plage, etc.).

    :param message: Message décrivant l'erreur de validation.
    :type message: str
    :param field_name: Nom du champ en cause.
    :type field_name: str | None
    :param details: Détails complémentaires sur l'erreur.
    :type details: str | None

    :Example:
        >>> raise ValidationError(
        ...     "Colonne obligatoire manquante",
        ...     field_name="date_appel",
        ... )
    """

    def __init__(
        self,
        message: str,
        field_name: str | None = None,
        details: str | None = None,
    ) -> None:
        """Initialise l'exception de validation.

        :param message: Message décrivant l'erreur.
        :type message: str
        :param field_name: Nom du champ en cause.
        :type field_name: str | None
        :param details: Détails complémentaires.
        :type details: str | None
        """
        self.field_name: str | None = field_name
        if field_name is not None and details is None:
            details = f"champ: {field_name}"
        elif field_name is not None and details is not None:
            details = f"champ: {field_name}, {details}"
        super().__init__(message=message, details=details)
