"""Module contenant l'extracteur CSV des appels entrants."""

from baobab_activity_reporting.ingestion.extractors.base_extractor import (
    BaseExtractor,
)
from baobab_activity_reporting.ingestion.extractors.csv_extraction_configuration import (
    CsvExtractionConfiguration,
)

_EXPECTED_COLUMNS: list[str] = [
    "Date",
    "Heure",
    "Agent",
    "Site",
    "Durée",
    "Statut",
]


class CsvIncomingCallsExtractor(BaseExtractor):
    """Extracteur spécialisé pour les fichiers CSV d'appels entrants.

    Utilise une configuration adaptée aux fichiers d'appels
    entrants du centre de contact.

    :Example:
        >>> extractor = CsvIncomingCallsExtractor()
        >>> result = extractor.extract("appels_entrants.csv")
    """

    def __init__(
        self,
        configuration: CsvExtractionConfiguration | None = None,
    ) -> None:
        """Initialise l'extracteur d'appels entrants.

        :param configuration: Configuration personnalisée. Si
            ``None``, la configuration par défaut est utilisée.
        :type configuration: CsvExtractionConfiguration | None
        """
        effective_config = (
            configuration if configuration is not None else self._build_configuration()
        )
        super().__init__(configuration=effective_config)

    def _build_configuration(self) -> CsvExtractionConfiguration:
        """Construit la configuration par défaut pour les appels entrants.

        :return: Configuration de lecture CSV.
        :rtype: CsvExtractionConfiguration
        """
        return CsvExtractionConfiguration(
            separator=";",
            encoding="utf-8",
            expected_columns=list(_EXPECTED_COLUMNS),
            source_label="appels_entrants",
        )
