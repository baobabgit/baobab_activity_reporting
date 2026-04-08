"""Tests pour FallbackSectionNarrativeWriter."""

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
from baobab_activity_reporting.reporting.fallback_section_narrative_writer import (
    FallbackSectionNarrativeWriter,
)
from baobab_activity_reporting.reporting.report_context import ReportContext
from baobab_activity_reporting.reporting.section_editorial_context import (
    SectionEditorialContext,
)


class TestFallbackSectionNarrativeWriter:
    """Tests unitaires pour FallbackSectionNarrativeWriter."""

    def _ctx(
        self,
        *,
        status: SectionStatus,
        objective: str,
        kpi_rows: list[dict[str, object]],
    ) -> SectionEditorialContext:
        """Construit un :class:`SectionEditorialContext` minimal."""
        ed = EditorialSectionDefinition(
            section_code="custom_unknown",
            section_title="Bloc",
            section_objective=objective,
            required_data=frozenset(),
            optional_data=frozenset(),
            display_rules=DisplayRules.default(),
            writing_style=WritingStyle.default(),
            visibility_rule=SectionVisibilityRule.from_prefixes(
                frozenset(),
                mandatory_in_report=False,
            ),
            table_policy=TablePolicy.default(),
        )
        p = ReportingPeriod(date(2026, 2, 1), date(2026, 2, 28))
        full = ReportContext(p, kpi_rows)
        return SectionEditorialContext.from_editorial(
            ed,
            "activity_by_agent",
            "2026-02-01",
            "2026-02-28",
            status,
            kpi_rows,
            full,
        )

    def test_degraded_message(self) -> None:
        """Mode dégradé : message sobre."""
        ctx = self._ctx(
            status=SectionStatus.DEGRADED,
            objective="",
            kpi_rows=[],
        )
        lines = FallbackSectionNarrativeWriter().write(ctx)
        assert len(lines) == 1
        assert "2026-02-01" in lines[0]

    def test_included_with_objective(self) -> None:
        """Section incluse avec objectif : pas de dump des codes KPI."""
        ctx = self._ctx(
            status=SectionStatus.INCLUDED,
            objective="Analyser le phénomène.",
            kpi_rows=[{"code": "x.y.z", "value": 1.0}],
        )
        lines = FallbackSectionNarrativeWriter().write(ctx)
        assert "Analyser le phénomène" in lines[0]
        assert "x.y.z" not in lines[0]
