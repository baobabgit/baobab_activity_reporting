"""Module contenant l'extracteur CSV des tickets."""

from baobab_activity_reporting.ingestion.extractors.base_extractor import (
    BaseExtractor,
)
from baobab_activity_reporting.ingestion.extractors.csv_extraction_configuration import (
    CsvExtractionConfiguration,
)

_EXPECTED_COLUMNS: list[str] = [
    "Numero Formulaire",
    "Date-Heure Depot Formulaire",
    "Date Dernier Envoi Demandeur",
    "Type Formulaire",
    "Numero Ticket",
    "Date-Heure Prise en Charge Ticket",
    "Date-Heure Creation Ticket",
    "Date-Heure Resolution Ticket",
    "Date-Heure Cloture Ticket",
    "Type Canal Ticket",
    "Nature Ticket",
    "Niveau Priorite Ticket",
    "Type Ticket",
    "Statut Ticket",
    "Type Contact",
    "Identifiant Contact",
    "Email Contact",
    "Telephone Secondaire Contact",
    "Telephone Principal Contact",
    "Groupe Creation Ticket",
    "Type GR Creation",
    "Domaine Creation Ticket",
    "Site Repartition Ticket",
    "Niveau Groupe Resolution",
    "Type Groupe Resolution",
    "Domaine Metier",
    "Nom Agent Proprietaire Ticket",
    "Prenom Agent Proprietaire Ticket",
    "Nom Agent Qualification Ticket",
    "Prenom Agent Qualification Ticket",
    "Site Agent Qualification Ticket",
    "Nom Agent Resolution Ticket",
    "Prenom Agent Resolution Ticket",
    "Groupe Qualification Ticket",
    "Niveau  GR Qualification",
    "Type GR  Qualification",
    "Domaine Qualification Ticket",
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
