"""Module contenant le résultat d'extraction."""


class ExtractionResult:
    """Résultat d'une opération d'extraction de données.

    Transporte les métadonnées issues de la lecture d'un
    fichier source sans exposer le ``DataFrame`` lui-même.

    :param source_name: Nom de la source extraite.
    :type source_name: str
    :param row_count: Nombre de lignes extraites.
    :type row_count: int
    :param column_names: Noms des colonnes extraites.
    :type column_names: list[str]
    :param errors: Messages d'erreur éventuels.
    :type errors: list[str]
    :param warnings: Messages d'avertissement éventuels.
    :type warnings: list[str]

    :Example:
        >>> result = ExtractionResult("appels.csv", 150, ["date", "agent"])
        >>> print(result.success)
        True
    """

    def __init__(
        self,
        source_name: str,
        row_count: int,
        column_names: list[str],
        errors: list[str] | None = None,
        warnings: list[str] | None = None,
    ) -> None:
        """Initialise le résultat d'extraction.

        :param source_name: Nom de la source.
        :type source_name: str
        :param row_count: Nombre de lignes extraites.
        :type row_count: int
        :param column_names: Noms des colonnes.
        :type column_names: list[str]
        :param errors: Messages d'erreur.
        :type errors: list[str] | None
        :param warnings: Messages d'avertissement.
        :type warnings: list[str] | None
        """
        self.source_name: str = source_name
        self.row_count: int = row_count
        self.column_names: list[str] = list(column_names)
        self.errors: list[str] = list(errors) if errors is not None else []
        self.warnings: list[str] = list(warnings) if warnings is not None else []

    @property
    def success(self) -> bool:
        """Indique si l'extraction s'est terminée sans erreur.

        :return: ``True`` si aucune erreur n'a été enregistrée.
        :rtype: bool
        """
        return len(self.errors) == 0

    def __repr__(self) -> str:
        """Retourne une représentation technique du résultat.

        :return: Représentation technique.
        :rtype: str
        """
        return (
            f"ExtractionResult("
            f"source_name={self.source_name!r}, "
            f"row_count={self.row_count!r}, "
            f"success={self.success!r})"
        )
