"""Module contenant l'indicateur de disponibilité de données."""


class DataAvailability:
    """Décrit la disponibilité d'un jeu de données.

    Permet d'évaluer si un jeu de données est suffisant
    pour alimenter une section de rapport.

    :param source_name: Nom de la source de données.
    :type source_name: str
    :param available: Indique si les données sont disponibles.
    :type available: bool
    :param row_count: Nombre de lignes disponibles.
    :type row_count: int
    :param reason: Raison de l'indisponibilité le cas échéant.
    :type reason: str | None

    :Example:
        >>> avail = DataAvailability("appels_entrants", True, 120)
        >>> print(avail.is_sufficient(min_rows=10))
        True
    """

    def __init__(
        self,
        source_name: str,
        available: bool,
        row_count: int = 0,
        reason: str | None = None,
    ) -> None:
        """Initialise l'indicateur de disponibilité.

        :param source_name: Nom de la source.
        :type source_name: str
        :param available: ``True`` si les données sont disponibles.
        :type available: bool
        :param row_count: Nombre de lignes disponibles.
        :type row_count: int
        :param reason: Raison de l'indisponibilité.
        :type reason: str | None
        """
        self.source_name: str = source_name
        self.available: bool = available
        self.row_count: int = row_count
        self.reason: str | None = reason

    def is_sufficient(self, min_rows: int = 1) -> bool:
        """Vérifie si le volume de données est suffisant.

        :param min_rows: Nombre minimal de lignes requises.
        :type min_rows: int
        :return: ``True`` si disponible et assez de lignes.
        :rtype: bool
        """
        return self.available and self.row_count >= min_rows

    def __repr__(self) -> str:
        """Retourne une représentation technique de la disponibilité.

        :return: Représentation technique.
        :rtype: str
        """
        return (
            f"DataAvailability("
            f"source_name={self.source_name!r}, "
            f"available={self.available!r}, "
            f"row_count={self.row_count!r})"
        )
