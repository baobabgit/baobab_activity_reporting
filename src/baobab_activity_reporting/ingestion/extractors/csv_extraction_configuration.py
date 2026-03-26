"""Module contenant la configuration d'extraction CSV."""


class CsvExtractionConfiguration:
    """Configuration de lecture d'un fichier CSV.

    Centralise les paramètres nécessaires à la lecture d'un
    fichier CSV par un extracteur : séparateur, encodage,
    colonnes attendues, etc.

    :param separator: Séparateur de colonnes.
    :type separator: str
    :param encoding: Encodage du fichier.
    :type encoding: str
    :param expected_columns: Colonnes attendues dans le fichier.
    :type expected_columns: list[str]
    :param skip_rows: Nombre de lignes à ignorer en début de fichier.
    :type skip_rows: int
    :param source_label: Libellé décrivant la source.
    :type source_label: str

    :Example:
        >>> config = CsvExtractionConfiguration(
        ...     separator=";",
        ...     encoding="utf-8",
        ...     expected_columns=["date", "agent"],
        ...     source_label="appels_entrants",
        ... )
    """

    def __init__(
        self,
        separator: str = ";",
        encoding: str = "utf-8",
        expected_columns: list[str] | None = None,
        skip_rows: int = 0,
        source_label: str = "csv",
    ) -> None:
        """Initialise la configuration d'extraction CSV.

        :param separator: Séparateur de colonnes.
        :type separator: str
        :param encoding: Encodage du fichier.
        :type encoding: str
        :param expected_columns: Colonnes attendues.
        :type expected_columns: list[str] | None
        :param skip_rows: Lignes à ignorer en début.
        :type skip_rows: int
        :param source_label: Libellé de la source.
        :type source_label: str
        """
        self.separator: str = separator
        self.encoding: str = encoding
        self.expected_columns: list[str] = (
            list(expected_columns) if expected_columns is not None else []
        )
        self.skip_rows: int = skip_rows
        self.source_label: str = source_label

    def __repr__(self) -> str:
        """Retourne une représentation technique de la configuration.

        :return: Représentation technique.
        :rtype: str
        """
        return (
            f"CsvExtractionConfiguration("
            f"separator={self.separator!r}, "
            f"encoding={self.encoding!r}, "
            f"source_label={self.source_label!r})"
        )
