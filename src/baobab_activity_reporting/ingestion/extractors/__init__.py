"""Sous-package des extracteurs CSV.

Regroupe l'extracteur abstrait et les extracteurs spécialisés.
"""

from baobab_activity_reporting.ingestion.extractors.base_extractor import (
    BaseExtractor,
)
from baobab_activity_reporting.ingestion.extractors.csv_extraction_configuration import (
    CsvExtractionConfiguration,
)
from baobab_activity_reporting.ingestion.extractors.csv_incoming_calls_extractor import (
    CsvIncomingCallsExtractor,
)
from baobab_activity_reporting.ingestion.extractors.csv_outgoing_calls_extractor import (
    CsvOutgoingCallsExtractor,
)
from baobab_activity_reporting.ingestion.extractors.csv_ticket_extractor import (
    CsvTicketExtractor,
)

__all__: list[str] = [
    "BaseExtractor",
    "CsvExtractionConfiguration",
    "CsvIncomingCallsExtractor",
    "CsvOutgoingCallsExtractor",
    "CsvTicketExtractor",
]
