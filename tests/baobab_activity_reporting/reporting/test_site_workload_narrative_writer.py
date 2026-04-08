"""Tests pour SiteWorkloadNarrativeWriter."""

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
from baobab_activity_reporting.reporting.site_workload_narrative_writer import (
    SiteWorkloadNarrativeWriter,
)


class TestSiteWorkloadNarrativeWriter:
    """Tests unitaires pour SiteWorkloadNarrativeWriter."""

    def test_two_sites(self) -> None:
        """Ventilation site sans codes techniques."""
        ed = EditorialSectionDefinition(
            section_code="weekly_site_workload",
            section_title="Sites",
            section_objective="",
            required_data=frozenset(),
            optional_data=frozenset(),
            display_rules=DisplayRules.default(),
            writing_style=WritingStyle.default(),
            visibility_rule=SectionVisibilityRule.from_prefixes(
                frozenset({"site."}),
                mandatory_in_report=False,
            ),
            table_policy=TablePolicy.default(),
        )
        p = ReportingPeriod(date(2026, 1, 1), date(2026, 1, 7))
        kpis = [
            {"code": "site.Nord.k", "value": 7.0},
            {"code": "site.Sud.k", "value": 3.0},
        ]
        full = ReportContext(p, kpis)
        ctx = SectionEditorialContext.from_editorial(
            ed,
            "weekly_activity_by_site",
            "2026-01-01",
            "2026-01-07",
            SectionStatus.INCLUDED,
            kpis,
            full,
        )
        paras = SiteWorkloadNarrativeWriter().write(ctx)
        assert "Nord" in " ".join(paras)
        assert "site.Nord" not in " ".join(paras)
