"""Cas d'usage : import des trois sources CSV vers SQLite."""

from __future__ import annotations

import logging
from pathlib import Path
from typing import Any

import pandas as pd

from baobab_activity_reporting.ingestion.extractors.base_extractor import (
    BaseExtractor,
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
from baobab_activity_reporting.processing.cleaning.telephony_communication_measure_filter import (
    filter_communication_duration_rows,
)
from baobab_activity_reporting.processing.kpi.consolidated_data_schema import (
    ConsolidatedDataSchema,
)
from baobab_activity_reporting.processing.normalization.standardization_pipeline import (
    StandardizationPipeline,
)
from baobab_activity_reporting.storage.repositories.prepared_data_repository import (
    PreparedDataRepository,
)
from baobab_activity_reporting.storage.repositories.raw_data_repository import (
    RawDataRepository,
)

logger = logging.getLogger(__name__)


class ImportSourcesUseCase:
    """Charge les CSV entrants, sortants et tickets puis persiste brut et préparé.

    Réutilise les extracteurs CSV existants, applique le pipeline de
    standardisation configuré, et remplace le contenu précédent des
    trois clés de :class:`ConsolidatedDataSchema`.

    :param raw_data_repository: Persistance des données brutes.
    :type raw_data_repository: RawDataRepository
    :param prepared_data_repository: Persistance des données préparées.
    :type prepared_data_repository: PreparedDataRepository
    :param standardization_pipeline: Normalisation post-lecture.
    :type standardization_pipeline: StandardizationPipeline
    :param incoming_extractor: Extracteur appels entrants (injectable).
    :type incoming_extractor: CsvIncomingCallsExtractor | None
    :param outgoing_extractor: Extracteur appels sortants (injectable).
    :type outgoing_extractor: CsvOutgoingCallsExtractor | None
    :param tickets_extractor: Extracteur tickets (injectable).
    :type tickets_extractor: CsvTicketExtractor | None
    """

    def __init__(
        self,
        raw_data_repository: RawDataRepository,
        prepared_data_repository: PreparedDataRepository,
        standardization_pipeline: StandardizationPipeline,
        *,
        incoming_extractor: CsvIncomingCallsExtractor | None = None,
        outgoing_extractor: CsvOutgoingCallsExtractor | None = None,
        tickets_extractor: CsvTicketExtractor | None = None,
    ) -> None:
        """Initialise le cas d'usage avec les repositories et le pipeline.

        :param raw_data_repository: Repository des données brutes.
        :type raw_data_repository: RawDataRepository
        :param prepared_data_repository: Repository des données préparées.
        :type prepared_data_repository: PreparedDataRepository
        :param standardization_pipeline: Pipeline de standardisation.
        :type standardization_pipeline: StandardizationPipeline
        :param incoming_extractor: Extracteur pour ``SOURCE_INCOMING_CALLS``.
        :type incoming_extractor: CsvIncomingCallsExtractor | None
        :param outgoing_extractor: Extracteur pour ``SOURCE_OUTGOING_CALLS``.
        :type outgoing_extractor: CsvOutgoingCallsExtractor | None
        :param tickets_extractor: Extracteur pour ``SOURCE_TICKETS``.
        :type tickets_extractor: CsvTicketExtractor | None
        """
        self._raw: RawDataRepository = raw_data_repository
        self._prepared: PreparedDataRepository = prepared_data_repository
        self._standardization: StandardizationPipeline = standardization_pipeline
        self._incoming: CsvIncomingCallsExtractor = (
            incoming_extractor if incoming_extractor is not None else CsvIncomingCallsExtractor()
        )
        self._outgoing: CsvOutgoingCallsExtractor = (
            outgoing_extractor if outgoing_extractor is not None else CsvOutgoingCallsExtractor()
        )
        self._tickets: CsvTicketExtractor = (
            tickets_extractor if tickets_extractor is not None else CsvTicketExtractor()
        )

    def execute(
        self,
        incoming_csv_path: str,
        outgoing_csv_path: str,
        tickets_csv_path: str,
    ) -> dict[str, Any]:
        """Importe les trois fichiers et retourne un résumé par source.

        :param incoming_csv_path: Chemin CSV appels entrants.
        :type incoming_csv_path: str
        :param outgoing_csv_path: Chemin CSV appels sortants.
        :type outgoing_csv_path: str
        :param tickets_csv_path: Chemin CSV tickets.
        :type tickets_csv_path: str
        :return: Clé ``sources`` : liste de résumés (clé, lignes, avertissements).
            Pour ``appels_entrants`` et ``appels_sortants``, clé additionnelle
            ``rows_excluded_non_communication_measure`` (lignes non « Durée de
            communication » retirées du jeu préparé).
        :rtype: dict[str, Any]
        """
        schema = ConsolidatedDataSchema
        triplet: tuple[tuple[str, str, BaseExtractor], ...] = (
            (incoming_csv_path, schema.SOURCE_INCOMING_CALLS, self._incoming),
            (outgoing_csv_path, schema.SOURCE_OUTGOING_CALLS, self._outgoing),
            (tickets_csv_path, schema.SOURCE_TICKETS, self._tickets),
        )
        summaries: list[dict[str, Any]] = []
        for path, source_key, extractor in triplet:
            summaries.append(self._ingest_file(path, source_key, extractor))
        logger.info("ImportSourcesUseCase terminé pour %d sources", len(summaries))
        return {"sources": summaries}

    def _ingest_file(
        self,
        path: str,
        source_key: str,
        extractor: BaseExtractor,
    ) -> dict[str, Any]:
        """Remplace le contenu d'une source : brut + préparé.

        :param path: Chemin du CSV.
        :type path: str
        :param source_key: Nom logique (:mod:`ConsolidatedDataSchema`).
        :type source_key: str
        :param extractor: Extracteur typé.
        :type extractor: BaseExtractor
        :return: Résumé d'import pour cette source.
        :rtype: dict[str, Any]
        """
        self._prepared.delete(source_key)
        self._raw.delete(source_key)
        dataframe_raw: pd.DataFrame = extractor.load_dataframe(path)
        source_name = Path(path).name
        extraction = extractor.extraction_result_from_dataframe(
            source_name,
            dataframe_raw,
        )
        raw_inserted = self._raw.save(dataframe_raw, source_key)
        prepared_frame: pd.DataFrame = self._standardization.run(dataframe_raw)
        excluded_measure = 0
        if source_key in (
            ConsolidatedDataSchema.SOURCE_INCOMING_CALLS,
            ConsolidatedDataSchema.SOURCE_OUTGOING_CALLS,
        ):
            prepared_frame, excluded_measure = filter_communication_duration_rows(
                prepared_frame,
            )
        prepared_inserted = self._prepared.save(prepared_frame, source_key)
        summary: dict[str, Any] = {
            "source_key": source_key,
            "file_name": source_name,
            "rows_raw_saved": raw_inserted,
            "rows_prepared_saved": prepared_inserted,
            "extraction_warnings": list(extraction.warnings),
        }
        if source_key in (
            ConsolidatedDataSchema.SOURCE_INCOMING_CALLS,
            ConsolidatedDataSchema.SOURCE_OUTGOING_CALLS,
        ):
            summary["rows_excluded_non_communication_measure"] = excluded_measure
        return summary
