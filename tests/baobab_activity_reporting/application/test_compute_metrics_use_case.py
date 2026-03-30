"""Tests pour ComputeMetricsUseCase."""

from datetime import date
from pathlib import Path

from baobab_activity_reporting.application.compute_metrics_use_case import (
    ComputeMetricsUseCase,
)
from baobab_activity_reporting.application.import_sources_use_case import (
    ImportSourcesUseCase,
)
from baobab_activity_reporting.domain.models.reporting_period import (
    ReportingPeriod,
)
from baobab_activity_reporting.processing.normalization.standardization_pipeline import (
    StandardizationPipeline,
)
from baobab_activity_reporting.storage.repositories.kpi_repository import (
    KpiRepository,
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


class TestComputeMetricsUseCase:
    """Tests du cas d'usage de calcul KPI."""

    def test_run_after_import(self, fixtures_dir: Path) -> None:
        """Enchaîne import puis calcul sur mars 2026."""
        mgr = DatabaseSessionManager(":memory:")
        try:
            raw_repo = RawDataRepository(mgr)
            prep_repo = PreparedDataRepository(mgr)
            kpi_repo = KpiRepository(mgr)
            ImportSourcesUseCase(
                raw_repo,
                prep_repo,
                StandardizationPipeline(),
            ).execute(
                str(fixtures_dir / "incoming_calls.csv"),
                str(fixtures_dir / "outgoing_calls.csv"),
                str(fixtures_dir / "tickets.csv"),
            )
            period = ReportingPeriod(date(2026, 3, 1), date(2026, 3, 31))
            summary = ComputeMetricsUseCase(prep_repo, kpi_repo).execute(period)
            assert int(summary["kpi_saved"]) > 0
        finally:
            mgr.close()
