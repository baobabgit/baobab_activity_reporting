"""Tests d'intégration pour KpiComputationPipeline."""

from datetime import date

import pandas as pd

from baobab_activity_reporting.domain.models.reporting_period import (
    ReportingPeriod,
)
from baobab_activity_reporting.processing.kpi.consolidated_data_schema import (
    ConsolidatedDataSchema,
)
from baobab_activity_reporting.processing.kpi.kpi_computation_pipeline import (
    KpiComputationPipeline,
)
from baobab_activity_reporting.storage.repositories.kpi_repository import (
    KpiRepository,
)
from baobab_activity_reporting.storage.repositories.prepared_data_repository import (
    PreparedDataRepository,
)
from baobab_activity_reporting.storage.sqlite.database_session_manager import (
    DatabaseSessionManager,
)


class TestKpiComputationPipeline:
    """Tests pour le pipeline de calcul KPI."""

    def test_full_run_persists_kpis(self) -> None:
        """Vérifie l'enchaînement complet jusqu'à SQLite."""
        mgr = DatabaseSessionManager(":memory:")
        try:
            prep = PreparedDataRepository(mgr)
            kpi_repo = KpiRepository(mgr)
            schema = ConsolidatedDataSchema
            inc = pd.DataFrame(
                {
                    "Date": ["2026-01-10"],
                    "Site": ["Paris"],
                    "Agent": ["Jean"],
                    "Durée": [120.0],
                }
            )
            out = pd.DataFrame(
                {
                    "Date": ["2026-01-11"],
                    "Site": ["Paris"],
                    "Agent": ["Jean"],
                    "Durée": [60.0],
                }
            )
            tickets = pd.DataFrame(
                {
                    "Date": ["2026-01-12"],
                    "Site": ["Paris"],
                    "Agent": ["Jean"],
                    "Canal": ["EFI"],
                }
            )
            prep.save(inc, schema.SOURCE_INCOMING_CALLS)
            prep.save(out, schema.SOURCE_OUTGOING_CALLS)
            prep.save(tickets, schema.SOURCE_TICKETS)
            period = ReportingPeriod(date(2026, 1, 1), date(2026, 1, 31))
            pipeline = KpiComputationPipeline(prep, kpi_repo, period)
            summary = pipeline.run()
            assert summary["kpi_saved"] > 0
            all_kpis = kpi_repo.load_all()
            assert len(all_kpis) == int(summary["kpi_saved"])
            codes = {row["code"] for row in all_kpis}
            assert "telephony.incoming.count" in codes
            assert any(c.startswith("tickets.channel.") for c in codes)
        finally:
            mgr.close()

    def test_replay_clears_period(self) -> None:
        """Vérifie la rejouabilité sans doublons sur la même période."""
        mgr = DatabaseSessionManager(":memory:")
        try:
            prep = PreparedDataRepository(mgr)
            kpi_repo = KpiRepository(mgr)
            schema = ConsolidatedDataSchema
            df = pd.DataFrame(
                {
                    "Date": ["2026-02-01"],
                    "Site": ["S"],
                    "Agent": ["A"],
                    "Durée": [1.0],
                }
            )
            prep.save(df, schema.SOURCE_INCOMING_CALLS)
            period = ReportingPeriod(date(2026, 2, 1), date(2026, 2, 28))
            pipe1 = KpiComputationPipeline(
                prep,
                kpi_repo,
                period,
                clear_existing_for_period=True,
            )
            n1 = int(pipe1.run()["kpi_saved"])
            pipe2 = KpiComputationPipeline(
                prep,
                kpi_repo,
                period,
                clear_existing_for_period=True,
            )
            n2 = int(pipe2.run()["kpi_saved"])
            assert n1 == n2
            assert len(kpi_repo.load_all()) == n2
        finally:
            mgr.close()
