"""Tests pour GenerateReportUseCase."""

from datetime import date

import pytest

from baobab_activity_reporting.application.generate_report_use_case import (
    GenerateReportUseCase,
)
from baobab_activity_reporting.domain.models.reporting_period import (
    ReportingPeriod,
)
from baobab_activity_reporting.exceptions.report_generation_error import (
    ReportGenerationError,
)
from baobab_activity_reporting.reporting.report_definition import ReportDefinition
from baobab_activity_reporting.storage.repositories.kpi_repository import (
    KpiRepository,
)
from baobab_activity_reporting.storage.sqlite.database_session_manager import (
    DatabaseSessionManager,
)


class TestGenerateReportUseCase:
    """Tests du cas d'usage de génération."""

    def test_build_from_persisted_kpis(self) -> None:
        """Construit un modèle à partir des KPI en base."""
        mgr = DatabaseSessionManager(":memory:")
        try:
            kpi_repo = KpiRepository(mgr)
            kpi_repo.save_kpi(
                "telephony.incoming.count",
                "Entrants",
                5.0,
                "appels",
                period_start="2026-03-01",
                period_end="2026-03-31",
            )
            kpi_repo.save_kpi(
                "tickets.channel.EFI.count",
                "EFI",
                2.0,
                "tickets",
                period_start="2026-03-01",
                period_end="2026-03-31",
            )
            period = ReportingPeriod(date(2026, 3, 1), date(2026, 3, 31))
            model = GenerateReportUseCase(kpi_repo).execute(
                period,
                ReportDefinition.activity_telephony(),
            )
            assert model.report_type == "activity_telephony"
            assert len(model.sections) == 2
        finally:
            mgr.close()

    def test_raises_when_no_eligible_section(self) -> None:
        """Période sans KPI : erreur métier."""
        mgr = DatabaseSessionManager(":memory:")
        try:
            kpi_repo = KpiRepository(mgr)
            period = ReportingPeriod(date(2026, 3, 1), date(2026, 3, 31))
            with pytest.raises(ReportGenerationError):
                GenerateReportUseCase(kpi_repo).execute(
                    period,
                    ReportDefinition.activity_telephony(),
                )
        finally:
            mgr.close()
