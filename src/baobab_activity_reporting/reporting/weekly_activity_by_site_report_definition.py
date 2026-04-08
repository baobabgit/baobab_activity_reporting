"""Fabrique de la définition du rapport hebdomadaire par site."""

from __future__ import annotations

from baobab_activity_reporting.reporting.editorial.display_rules import DisplayRules
from baobab_activity_reporting.reporting.editorial.editorial_section_definition import (
    EditorialSectionDefinition,
)
from baobab_activity_reporting.reporting.editorial.section_visibility_rule import (
    SectionVisibilityRule,
)
from baobab_activity_reporting.reporting.editorial.table_policy import TablePolicy
from baobab_activity_reporting.reporting.editorial.writing_style import WritingStyle
from baobab_activity_reporting.reporting.report_definition import ReportDefinition


class WeeklyActivityBySiteReportDefinition:
    """Construit le gabarit ``weekly_activity_by_site`` (plan éditorial 6 sections).

    La section « Répartition de l'activité » est centrée sur la charge par site.
    """

    @staticmethod
    def build() -> ReportDefinition:
        """Assemble :class:`ReportDefinition` pour le rapport hebdomadaire site.

        :return: Définition complète avec six sections ordonnées.
        :rtype: ReportDefinition
        """
        dr = DisplayRules.default()
        ws = WritingStyle.default()
        tp_std = TablePolicy.default()
        tp_sorted = TablePolicy(
            max_rows=None,
            sort_by_numeric_value_desc=True,
            include_site_agent_channel_columns=True,
        )
        sections: tuple[EditorialSectionDefinition, ...] = (
            EditorialSectionDefinition(
                section_code="weekly_synthesis",
                section_title="Synthèse hebdomadaire",
                section_objective=(
                    "Donner en quelques phrases la lecture globale de la semaine "
                    "sur les volumes téléphoniques et le traitement des tickets."
                ),
                required_data=frozenset({"slot.period.summary"}),
                optional_data=frozenset(
                    {"slot.telephony", "slot.tickets", "slot.agent", "slot.site"},
                ),
                display_rules=dr,
                writing_style=ws,
                visibility_rule=SectionVisibilityRule.from_prefixes(
                    frozenset(),
                    mandatory_in_report=True,
                ),
                table_policy=tp_std,
            ),
            EditorialSectionDefinition(
                section_code="weekly_telephony",
                section_title="Activité téléphonique",
                section_objective=(
                    "Décrire les volumes et durées d'appels entrants et sortants " "sur la période."
                ),
                required_data=frozenset({"slot.telephony.global"}),
                optional_data=frozenset(),
                display_rules=dr,
                writing_style=ws,
                visibility_rule=SectionVisibilityRule.from_prefixes(
                    frozenset({"telephony."}),
                    mandatory_in_report=False,
                ),
                table_policy=tp_sorted,
            ),
            EditorialSectionDefinition(
                section_code="weekly_ticket_processing",
                section_title="Activité de traitement",
                section_objective=(
                    "Présenter le travail sur les tickets : volumes par canal "
                    "et charges associées."
                ),
                required_data=frozenset({"slot.tickets.channels"}),
                optional_data=frozenset({"slot.tickets.by_site"}),
                display_rules=dr,
                writing_style=ws,
                visibility_rule=SectionVisibilityRule.from_prefixes(
                    frozenset({"tickets."}),
                    mandatory_in_report=False,
                ),
                table_policy=tp_sorted,
            ),
            EditorialSectionDefinition(
                section_code="weekly_site_workload",
                section_title="Répartition de l'activité",
                section_objective=(
                    "Analyser la répartition de la charge entre les sites sur "
                    "la téléphonie et les tickets."
                ),
                required_data=frozenset({"slot.site.breakdown"}),
                optional_data=frozenset({"slot.agent"}),
                display_rules=dr,
                writing_style=ws,
                visibility_rule=SectionVisibilityRule.from_prefixes(
                    frozenset({"site."}),
                    mandatory_in_report=False,
                ),
                table_policy=tp_sorted,
            ),
            EditorialSectionDefinition(
                section_code="weekly_attention_points",
                section_title="Points d'attention",
                section_objective=(
                    "Signaler les déséquilibres ou anomalies visibles dans les "
                    "indicateurs (sans préjuger de la cause)."
                ),
                required_data=frozenset(),
                optional_data=frozenset({"slot.telephony", "slot.tickets"}),
                display_rules=DisplayRules(
                    show_metric_tables=True,
                    collapse_empty_dimensions=True,
                    emphasize_variance=True,
                ),
                writing_style=WritingStyle(
                    tone="professionnel",
                    perspective="tiers",
                    length_hint="bref",
                ),
                visibility_rule=SectionVisibilityRule.from_prefixes(
                    frozenset({"telephony.", "tickets."}),
                    mandatory_in_report=False,
                ),
                table_policy=tp_std,
            ),
            EditorialSectionDefinition(
                section_code="weekly_conclusion",
                section_title="Conclusion",
                section_objective=(
                    "Clore le rapport par une formulation neutre rappelant "
                    "l'horizon temporel couvert."
                ),
                required_data=frozenset({"slot.period.bounds"}),
                optional_data=frozenset(),
                display_rules=DisplayRules(
                    show_metric_tables=False,
                    collapse_empty_dimensions=True,
                    emphasize_variance=False,
                ),
                writing_style=ws,
                visibility_rule=SectionVisibilityRule.from_prefixes(
                    frozenset(),
                    mandatory_in_report=True,
                ),
                table_policy=tp_std,
            ),
        )
        return ReportDefinition(
            report_type="weekly_activity_by_site",
            title_template="Activité hebdomadaire par site — du {period_start} au {period_end}",
            editorial_sections=sections,
        )
