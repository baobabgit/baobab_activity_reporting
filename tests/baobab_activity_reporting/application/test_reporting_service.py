"""Tests d'intégration pour ReportingService."""

from datetime import date
from pathlib import Path

from baobab_activity_reporting.application.reporting_service import ReportingService
from baobab_activity_reporting.domain.models.reporting_period import (
    ReportingPeriod,
)
from baobab_activity_reporting.reporting.report_definition import ReportDefinition


class TestReportingService:
    """Tests de la façade applicative."""

    def test_full_chain_import_compute_generate(
        self,
        tmp_path: Path,
        fixtures_dir: Path,
    ) -> None:
        """Enchaîne import, calcul et génération avec export Markdown."""
        db_file = tmp_path / "app.db"
        md_out = tmp_path / "out.md"
        service = ReportingService(str(db_file))
        try:
            service.import_sources(
                str(fixtures_dir / "incoming_calls.csv"),
                str(fixtures_dir / "outgoing_calls.csv"),
                str(fixtures_dir / "tickets.csv"),
            )
            period = ReportingPeriod(date(2026, 3, 1), date(2026, 3, 31))
            service.compute_metrics(period, clear_existing_for_period=True)
            model = service.generate_report(
                period,
                ReportDefinition.activity_telephony(),
                markdown_path=str(md_out),
            )
            assert model.report_type == "activity_telephony"
            text = md_out.read_text(encoding="utf-8")
            assert "Activité" in text or "téléphonique" in text
        finally:
            service.close()
