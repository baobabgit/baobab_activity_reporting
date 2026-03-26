"""Module contenant l'extracteur CSV des tickets."""

from baobab_activity_reporting.ingestion.extractors.base_extractor import (
    BaseExtractor,
)
from baobab_activity_reporting.ingestion.extractors.csv_extraction_configuration import (
    CsvExtractionConfiguration,
)

_EXPECTED_COLUMNS: list[str] = [
    "Numéro",
    "Date",
    "Agent",
    "Site",
    "Canal",
    "Catégorie",
]


class CsvTicketExtractor(BaseExtractor):
    """Extracteur spécialisé pour les fichiers CSV de tickets.

    Utilise une configuration adaptée aux fichiers de tickets
    du centre de contact (EFI, EDI, téléphone, etc.).

    :Example:
        >>> extractor = CsvTicketExtractor()
        >>> result = extractor.extract("tickets.csv")
    """

    def __init__(
        self,
        configuration: CsvExtractionConfiguration | None = None,
    ) -> None:
        """Initialise l'extracteur de tickets.

        :param configuration: Configuration personnalisée. Si
            ``None``, la configuration par défaut est utilisée.
        :type configuration: CsvExtractionConfiguration | None
        """
        effective_config = (
            configuration if configuration is not None else self._build_configuration()
        )
        super().__init__(configuration=effective_config)

    def _build_configuration(self) -> CsvExtractionConfiguration:
        """Construit la configuration par défaut pour les tickets.

        :return: Configuration de lecture CSV.
        :rtype: CsvExtractionConfiguration
        """
        return CsvExtractionConfiguration(
            separator=";",
            encoding="utf-8",
            expected_columns=list(_EXPECTED_COLUMNS),
            source_label="tickets",
        )
