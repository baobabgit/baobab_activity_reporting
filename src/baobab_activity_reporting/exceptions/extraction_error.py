"""Module contenant l'exception d'extraction."""

from baobab_activity_reporting.exceptions.reporting_error import (
    ReportingError,
)


class ExtractionError(ReportingError):
    """Exception levée lors d'une erreur d'extraction de données.

    Hérite de :class:`ReportingError` et représente les erreurs
    survenant lors de la lecture des fichiers sources (fichier
    introuvable, encodage invalide, format inattendu, etc.).

    :param message: Message décrivant l'erreur d'extraction.
    :type message: str
    :param source_name: Nom de la source en cause.
    :type source_name: str | None
    :param details: Détails complémentaires sur l'erreur.
    :type details: str | None

    :Example:
        >>> raise ExtractionError(
        ...     "Fichier introuvable",
        ...     source_name="appels_entrants.csv",
        ... )
    """

    def __init__(
        self,
        message: str,
        source_name: str | None = None,
        details: str | None = None,
    ) -> None:
        """Initialise l'exception d'extraction.

        :param message: Message décrivant l'erreur.
        :type message: str
        :param source_name: Nom de la source en cause.
        :type source_name: str | None
        :param details: Détails complémentaires.
        :type details: str | None
        """
        self.source_name: str | None = source_name
        if source_name is not None and details is None:
            details = f"source: {source_name}"
        elif source_name is not None and details is not None:
            details = f"source: {source_name}, {details}"
        super().__init__(message=message, details=details)
