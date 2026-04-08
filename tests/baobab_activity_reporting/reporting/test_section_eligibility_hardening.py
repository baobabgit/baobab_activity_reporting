"""Scénarios d'intégration pour l'éligibilité renforcée."""

from datetime import date

from baobab_activity_reporting.domain.models.reporting_period import (
    ReportingPeriod,
)
from baobab_activity_reporting.domain.results.section_decision import SectionStatus
from baobab_activity_reporting.domain.results.section_eligibility_codes import (
    SectionEligibilityCodes,
)
from baobab_activity_reporting.reporting.report_context import ReportContext
from baobab_activity_reporting.reporting.report_definition import ReportDefinition
from baobab_activity_reporting.reporting.report_planner import ReportPlanner
from baobab_activity_reporting.reporting.section_eligibility_evaluator import (
    SectionEligibilityEvaluator,
)


class TestSectionEligibilityHardening:
    """Comportements hebdo agent/site et conclusion."""

    def test_weekly_agent_tickets_excluded_without_channel_volume(self) -> None:
        """Traitement ticket absent sans KPI canaux exploitables."""
        p = ReportingPeriod(date(2026, 4, 1), date(2026, 4, 7))
        ctx = ReportContext(
            p,
            [
                {"code": "telephony.incoming.count", "value": 1.0},
                {"code": "telephony.outgoing.count", "value": 1.0},
            ],
        )
        included, decisions = ReportPlanner().plan(
            ReportDefinition.weekly_activity_by_agent(),
            ctx,
        )
        codes_in = {ed.section_code for ed, _ in included}
        assert "weekly_ticket_processing" not in codes_in
        by_code = {d.section_code: d for d in decisions}
        assert by_code["weekly_ticket_processing"].status == SectionStatus.EXCLUDED

    def test_weekly_attention_included_on_imbalance(self) -> None:
        """Points d'attention présents si déséquilibre téléphonie."""
        p = ReportingPeriod(date(2026, 4, 1), date(2026, 4, 7))
        ctx = ReportContext(
            p,
            [
                {"code": "telephony.incoming.count", "value": 40.0},
                {"code": "telephony.outgoing.count", "value": 2.0},
            ],
        )
        included, _ = ReportPlanner().plan(
            ReportDefinition.weekly_activity_by_site(),
            ctx,
        )
        codes_in = {ed.section_code for ed, _ in included}
        assert "weekly_attention_points" in codes_in

    def test_weekly_conclusion_excluded_without_exploitable_peers(self) -> None:
        """Conclusion absente si aucune section à contenu."""
        ev = SectionEligibilityEvaluator()
        p = ReportingPeriod(date(2026, 4, 1), date(2026, 4, 7))
        ctx = ReportContext(p, [])
        conclusion = next(
            s
            for s in ReportDefinition.weekly_activity_by_agent().editorial_sections
            if s.section_code == "weekly_conclusion"
        )
        d = ev.evaluate_editorial_section(
            conclusion,
            ctx,
            peer_exploitable_included=frozenset(),
        )
        assert d.status == SectionStatus.EXCLUDED
        assert SectionEligibilityCodes.EXCLUDED_NO_EXPLOITABLE_PEER_SECTIONS in (
            d.detail.codes if d.detail else frozenset()
        )

    def test_weekly_conclusion_included_with_peer(self) -> None:
        """Conclusion si une section exploitable est incluse."""
        ev = SectionEligibilityEvaluator()
        p = ReportingPeriod(date(2026, 4, 1), date(2026, 4, 7))
        ctx = ReportContext(p, [])
        conclusion = next(
            s
            for s in ReportDefinition.weekly_activity_by_agent().editorial_sections
            if s.section_code == "weekly_conclusion"
        )
        d = ev.evaluate_editorial_section(
            conclusion,
            ctx,
            peer_exploitable_included=frozenset({"weekly_telephony"}),
        )
        assert d.status == SectionStatus.INCLUDED
        assert d.detail is not None
        assert SectionEligibilityCodes.CONCLUSION_ALLOWED in d.detail.codes

    def test_weekly_site_workload_excluded_single_site(self) -> None:
        """Répartition site exclue avec un seul site mesuré."""
        p = ReportingPeriod(date(2026, 4, 1), date(2026, 4, 7))
        ctx = ReportContext(
            p,
            [
                {"code": "telephony.incoming.count", "value": 1.0},
                {"code": "telephony.outgoing.count", "value": 1.0},
                {"code": "site.Paris.telephony.incoming.count", "value": 1.0},
            ],
        )
        included, _ = ReportPlanner().plan(
            ReportDefinition.weekly_activity_by_site(),
            ctx,
        )
        codes_in = {ed.section_code for ed, _ in included}
        assert "weekly_site_workload" not in codes_in
