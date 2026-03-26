"""Module contenant l'exception de rendu documentaire."""

from baobab_activity_reporting.exceptions.reporting_error import (
    ReportingError,
)


class WriterError(ReportingError):
    """Exception levée lors d'une erreur de rendu documentaire.

    Hérite de :class:`ReportingError` et représente les erreurs
    survenant lors de l'export du rapport vers un format de
    sortie (DOCX, Markdown, HTML, etc.).

    :param message: Message décrivant l'erreur de rendu.
    :type message: str
    :param output_format: Format de sortie en cause.
    :type output_format: str | None
    :param details: Détails complémentaires sur l'erreur.
    :type details: str | None

    :Example:
        >>> raise WriterError(
        ...     "Échec de l'export DOCX",
        ...     output_format="docx",
        ... )
    """

    def __init__(
        self,
        message: str,
        output_format: str | None = None,
        details: str | None = None,
    ) -> None:
        """Initialise l'exception de rendu.

        :param message: Message décrivant l'erreur.
        :type message: str
        :param output_format: Format de sortie en cause.
        :type output_format: str | None
        :param details: Détails complémentaires.
        :type details: str | None
        """
        self.output_format: str | None = output_format
        if output_format is not None and details is None:
            details = f"format: {output_format}"
        elif output_format is not None and details is not None:
            details = f"format: {output_format}, {details}"
        super().__init__(message=message, details=details)
