"""Tests pour SectionEditorialContext."""

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


class TestSectionEditorialContext:
    """Tests unitaires pour SectionEditorialContext."""

    def test_from_editorial_copies_rows(self) -> None:
        """Les lignes KPI sont copiées (immuabilité)."""
        ed = EditorialSectionDefinition(
            section_code="weekly_synthesis",
            section_title="Synthèse",
            section_objective="",
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
        p = ReportingPeriod(date(2026, 1, 1), date(2026, 1, 7))
        kpi = [{"code": "telephony.incoming.count", "value": 1.0}]
        full = ReportContext(p, kpi)
        ctx = SectionEditorialContext.from_editorial(
            ed,
            "weekly_activity_by_site",
            "2026-01-01",
            "2026-01-07",
            SectionStatus.INCLUDED,
            kpi,
            full,
        )
        assert ctx.report_type == "weekly_activity_by_site"
        assert ctx.kpi_rows[0]["value"] == 1.0
        kpi[0]["value"] = 99.0
        assert ctx.kpi_rows[0]["value"] == 1.0
