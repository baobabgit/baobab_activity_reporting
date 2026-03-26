"""Module contenant le modèle de période de reporting."""

from datetime import date

from baobab_activity_reporting.exceptions.validation_error import (
    ValidationError,
)


class ReportingPeriod:
    """Représente une période de reporting bornée par deux dates.

    Encapsule la date de début et la date de fin d'une période
    sur laquelle les indicateurs d'activité sont calculés.

    :param start_date: Date de début de la période (incluse).
    :type start_date: date
    :param end_date: Date de fin de la période (incluse).
    :type end_date: date

    :raises ValidationError: Si la date de fin est antérieure
        à la date de début.

    :Example:
        >>> from datetime import date
        >>> period = ReportingPeriod(date(2026, 1, 1), date(2026, 1, 31))
        >>> print(period.duration_days)
        31
    """

    def __init__(self, start_date: date, end_date: date) -> None:
        """Initialise la période de reporting.

        :param start_date: Date de début de la période.
        :type start_date: date
        :param end_date: Date de fin de la période.
        :type end_date: date
        :raises ValidationError: Si ``end_date < start_date``.
        """
        if end_date < start_date:
            raise ValidationError(
                "La date de fin est antérieure à la date de début",
                field_name="end_date",
                details=f"{start_date} > {end_date}",
            )
        self.start_date: date = start_date
        self.end_date: date = end_date

    @property
    def duration_days(self) -> int:
        """Retourne le nombre de jours de la période (bornes incluses).

        :return: Nombre de jours.
        :rtype: int
        """
        return (self.end_date - self.start_date).days + 1

    def contains(self, a_date: date) -> bool:
        """Vérifie si une date est comprise dans la période.

        :param a_date: Date à vérifier.
        :type a_date: date
        :return: ``True`` si la date est dans la période.
        :rtype: bool
        """
        return self.start_date <= a_date <= self.end_date

    def __eq__(self, other: object) -> bool:
        """Vérifie l'égalité entre deux périodes.

        :param other: Objet à comparer.
        :type other: object
        :return: ``True`` si les périodes sont identiques.
        :rtype: bool
        """
        if not isinstance(other, ReportingPeriod):
            return NotImplemented
        return self.start_date == other.start_date and self.end_date == other.end_date

    def __repr__(self) -> str:
        """Retourne une représentation technique de la période.

        :return: Représentation technique.
        :rtype: str
        """
        return (
            f"ReportingPeriod(" f"start_date={self.start_date!r}, " f"end_date={self.end_date!r})"
        )
