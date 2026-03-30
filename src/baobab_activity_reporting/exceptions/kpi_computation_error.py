"""Module contenant l'erreur de calcul des KPI."""

from baobab_activity_reporting.exceptions.reporting_error import (
    ReportingError,
)


class KpiComputationError(ReportingError):
    """Erreur métier ou technique lors du calcul des indicateurs.

    Levée lorsque les données consolidées sont insuffisantes, que des
    colonnes attendues sont absentes, ou qu'une étape d'agrégation est
    invalide.

    :param message: Description de l'erreur.
    :type message: str
    :param details: Informations complémentaires (colonne, source, etc.).
    :type details: str | None

    :Example:
        >>> raise KpiComputationError(
        ...     "Colonne de date introuvable",
        ...     details="DataFrame vide ou sans colonne Date/date",
        ... )
    """

    def __init__(
        self,
        message: str,
        details: str | None = None,
    ) -> None:
        """Initialise l'erreur de calcul KPI.

        :param message: Description de l'erreur.
        :type message: str
        :param details: Détails optionnels.
        :type details: str | None
        """
        super().__init__(message=message, details=details)
