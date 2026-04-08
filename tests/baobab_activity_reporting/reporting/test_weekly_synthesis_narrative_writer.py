"""Tests pour WeeklySynthesisNarrativeWriter."""

from datetime import date

from baobab_activity_reporting.domain.models.reporting_period import (
    ReportingPeriod,
)
from baobab_activity_reporting.domain.results.section_decision import SectionStatus
from baobab_activity_reporting.reporting.editorial.display_rules import DisplayRules
from baobab_activity_reporting.reporting.editorial.editorial_section_definition import (
    EditorialSectionDefinition,
)
from baobab_activity_reporting.reporting.editorial.section_visibility_rule import (
    SectionVisibilityRule,
)
from baobab_activity_reporting.reporting.editorial.table_policy import TablePolicy
from baobab_activity_reporting.reporting.editorial.writing_style import WritingStyle
from baobab_activity_reporting.reporting.report_context import ReportContext
from baobab_activity_reporting.reporting.section_editorial_context import (
    SectionEditorialContext,
)
from baobab_activity_reporting.reporting.weekly_synthesis_narrative_writer import (
    WeeklySynthesisNarrativeWriter,
)


class TestWeeklySynthesisNarrativeWriter:
    """Tests unitaires pour WeeklySynthesisNarrativeWriter."""

    def _editorial(self) -> EditorialSectionDefinition:
        """Définition type synthèse hebdo."""
        return EditorialSectionDefinition(
            section_code="weekly_synthesis",
            section_title="Synthèse hebdomadaire",
            section_objective="Vue globale.",
            required_data=frozenset(),
            optional_data=frozenset(),
            display_rules=DisplayRules.default(),
            writing_style=WritingStyle.default(),
            visibility_rule=SectionVisibilityRule.from_prefixes(
                frozenset(),
                mandatory_in_report=True,
            ),
            table_policy=TablePolicy.default(),
        )

    def test_synthesis_agent_report_telephony_only(self) -> None:
        """Rapport hebdo agent : variante téléphonie seule."""
        p = ReportingPeriod(date(2026, 3, 1), date(2026, 3, 7))
        kpis = [
            {"code": "telephony.incoming.count", "value": 8.0},
            {"code": "telephony.outgoing.count", "value": 2.0},
        ]
        full = ReportContext(p, kpis)
        ctx = SectionEditorialContext.from_editorial(
            self._editorial(),
            "weekly_activity_by_agent",
            "2026-03-01",
            "2026-03-07",
            SectionStatus.INCLUDED,
            kpis,
            full,
        )
        paras = WeeklySynthesisNarrativeWriter().write(ctx)
        assert len(paras) == 2
        joined = " ".join(paras).lower()
        assert "ticket" in joined or "tickets" in joined
        assert "téléphon" in joined or "telephon" in joined

    def test_synthesis_site_report_tickets_only(self) -> None:
        """Rapport hebdo site : variante tickets seuls."""
        p = ReportingPeriod(date(2026, 3, 1), date(2026, 3, 7))
        kpis = [
            {"code": "tickets.channel.A.count", "label": "A", "value": 10.0},
        ]
        full = ReportContext(p, kpis)
        ctx = SectionEditorialContext.from_editorial(
            self._editorial(),
            "weekly_activity_by_site",
            "2026-03-01",
            "2026-03-07",
            SectionStatus.INCLUDED,
            kpis,
            full,
        )
        paras = WeeklySynthesisNarrativeWriter().write(ctx)
        assert len(paras) == 2
        assert "tickets.channel" not in " ".join(paras)
