"""Tests pour AttentionPointsInsightWriter."""

from datetime import date

from baobab_activity_reporting.domain.models.reporting_period import (
    ReportingPeriod,
)
from baobab_activity_reporting.domain.results.section_decision import SectionStatus
from baobab_activity_reporting.domain.results.section_eligibility_codes import (
    SectionEligibilityCodes,
)
from baobab_activity_reporting.domain.results.section_eligibility_detail import (
    SectionEligibilityDetail,
)
from baobab_activity_reporting.reporting.attention_points_insight_writer import (
    AttentionPointsInsightWriter,
)
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


class TestAttentionPointsInsightWriter:
    """Tests unitaires pour AttentionPointsInsightWriter."""

    def _base_editorial(self) -> EditorialSectionDefinition:
        """Section minimaliste pour construire le contexte."""
        return EditorialSectionDefinition(
            section_code="weekly_attention_points",
            section_title="Points d'attention",
            section_objective="Vigilance.",
            required_data=frozenset(),
            optional_data=frozenset(),
            display_rules=DisplayRules.default(),
            writing_style=WritingStyle.default(),
            visibility_rule=SectionVisibilityRule.from_prefixes(
                frozenset({"telephony."}),
                mandatory_in_report=False,
            ),
            table_policy=TablePolicy.default(),
        )

    def test_empty_when_no_detail(self) -> None:
        """Sans détail d'éligibilité, aucun insight."""
        p = ReportingPeriod(date(2026, 1, 1), date(2026, 1, 7))
        ctx_full = ReportContext(p, [])
        sec = SectionEditorialContext.from_editorial(
            self._base_editorial(),
            "weekly_activity_by_agent",
            "2026-01-01",
            "2026-01-07",
            SectionStatus.INCLUDED,
            [],
            ctx_full,
            eligibility_detail=None,
        )
        assert AttentionPointsInsightWriter().write(sec) == []

    def test_imbalance_editorial_with_ratio(self) -> None:
        """Déséquilibre téléphonie : phrase avec ratio, sans code KPI."""
        p = ReportingPeriod(date(2026, 1, 1), date(2026, 1, 7))
        kpis = [
            {"code": "telephony.incoming.count", "value": 50.0},
            {"code": "telephony.outgoing.count", "value": 5.0},
        ]
        ctx_full = ReportContext(p, kpis)
        detail = SectionEligibilityDetail(
            codes=frozenset({SectionEligibilityCodes.ATTENTION_IMBALANCE_TELEPHONY}),
            notes=("test",),
        )
        sec = SectionEditorialContext.from_editorial(
            self._base_editorial(),
            "weekly_activity_by_agent",
            "2026-01-01",
            "2026-01-07",
            SectionStatus.INCLUDED,
            kpis,
            ctx_full,
            eligibility_detail=detail,
        )
        out = AttentionPointsInsightWriter().write(sec)
        assert len(out) == 1
        assert "ratio" in out[0].lower()
        assert "telephony." not in out[0]

    def test_channel_dominance_editorial(self) -> None:
        """Canal dominant : libellé métier uniquement."""
        p = ReportingPeriod(date(2026, 1, 1), date(2026, 1, 7))
        kpis = [
            {"code": "tickets.channel.EFI.count", "label": "EFI", "value": 90.0},
            {"code": "tickets.channel.EDI.count", "label": "EDI", "value": 10.0},
        ]
        ctx_full = ReportContext(p, kpis)
        detail = SectionEligibilityDetail(
            codes=frozenset({SectionEligibilityCodes.ATTENTION_TICKET_CHANNEL_DOMINANCE}),
            notes=("test",),
        )
        sec = SectionEditorialContext.from_editorial(
            self._base_editorial(),
            "weekly_activity_by_agent",
            "2026-01-01",
            "2026-01-07",
            SectionStatus.INCLUDED,
            kpis,
            ctx_full,
            eligibility_detail=detail,
        )
        out = AttentionPointsInsightWriter().write(sec)
        assert any("EFI" in line for line in out)
        assert not any("tickets.channel" in line for line in out)
