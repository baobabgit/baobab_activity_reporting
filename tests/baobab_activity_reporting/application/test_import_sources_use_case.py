"""Tests pour ImportSourcesUseCase."""

from pathlib import Path

from baobab_activity_reporting.application.import_sources_use_case import (
    ImportSourcesUseCase,
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
from baobab_activity_reporting.storage.sqlite.database_session_manager import (
    DatabaseSessionManager,
)


class TestImportSourcesUseCase:
    """Tests du cas d'usage d'import."""

    def test_import_three_fixtures(self, fixtures_dir: Path) -> None:
        """Importe les trois CSV de fixtures et remplit brut / préparé."""
        mgr = DatabaseSessionManager(":memory:")
        try:
            raw_repo = RawDataRepository(mgr)
            prep_repo = PreparedDataRepository(mgr)
            uc = ImportSourcesUseCase(
                raw_repo,
                prep_repo,
                StandardizationPipeline(),
            )
            summary = uc.execute(
                str(fixtures_dir / "incoming_calls.csv"),
                str(fixtures_dir / "outgoing_calls.csv"),
                str(fixtures_dir / "tickets.csv"),
            )
            sources = summary["sources"]
            assert len(sources) == 3
            schema = ConsolidatedDataSchema
            by_key = {s["source_key"]: s for s in sources}
            for key in (
                schema.SOURCE_INCOMING_CALLS,
                schema.SOURCE_OUTGOING_CALLS,
                schema.SOURCE_TICKETS,
            ):
                assert prep_repo.count(key) > 0
                assert raw_repo.count(key) > 0
            for tel in (schema.SOURCE_INCOMING_CALLS, schema.SOURCE_OUTGOING_CALLS):
                assert "rows_excluded_non_communication_measure" in by_key[tel]
                assert by_key[tel]["rows_excluded_non_communication_measure"] == 0
            assert "rows_excluded_non_communication_measure" not in by_key[
                schema.SOURCE_TICKETS
            ]
        finally:
            mgr.close()
