"""Module orchestrant planification et construction du ReportModel."""

import logging

from baobab_activity_reporting.domain.results.section_decision import SectionStatus
from baobab_activity_reporting.exceptions.report_generation_error import (
    ReportGenerationError,
)
from baobab_activity_reporting.reporting.editorial.editorial_section_definition import (
    EditorialSectionDefinition,
)
from baobab_activity_reporting.reporting.insight_builder import InsightBuilder
from baobab_activity_reporting.reporting.narrative_builder import NarrativeBuilder
from baobab_activity_reporting.reporting.report_context import ReportContext
from baobab_activity_reporting.reporting.report_definition import ReportDefinition
from baobab_activity_reporting.reporting.report_model import ReportModel
from baobab_activity_reporting.reporting.report_planner import ReportPlanner
from baobab_activity_reporting.reporting.table_builder import TableBuilder

logger = logging.getLogger(__name__)

_INSIGHT_TELEPHONY_CODES = frozenset({"telephony_overview", "weekly_telephony"})
_INSIGHT_CHANNEL_CODES = frozenset({"ticket_channels", "weekly_ticket_processing"})


class ReportBuilder:
    """Assemble plan, narratifs, tableaux et insights en :class:`ReportModel`.

    :param planner: Planificateur injectable.
    :type planner: ReportPlanner | None
    :param narrative_builder: Constructeur de narratifs.
    :type narrative_builder: NarrativeBuilder | None
    :param table_builder: Constructeur de tableaux.
    :type table_builder: TableBuilder | None
    :param insight_builder: Constructeur d'insights.
    :type insight_builder: InsightBuilder | None

    :Example:
        >>> from datetime import date
        >>> from baobab_activity_reporting.domain.models.reporting_period import (
        ...     ReportingPeriod,
        ... )
        >>> from baobab_activity_reporting.reporting.report_context import (
        ...     ReportContext,
        ... )
        >>> from baobab_activity_reporting.reporting.report_definition import (
        ...     ReportDefinition,
        ... )
        >>> from baobab_activity_reporting.reporting.report_builder import (
        ...     ReportBuilder,
        ... )
        >>> p = ReportingPeriod(date(2026, 1, 1), date(2026, 1, 31))
        >>> ctx = ReportContext(
        ...     p,
        ...     [{"code": "telephony.incoming.count", "label": "E", "value": 3.0}],
        ... )
        >>> model = ReportBuilder().build(ReportDefinition.activity_telephony(), ctx)
        >>> model.section_codes
        ['telephony_overview']
    """

    def __init__(
        self,
        planner: ReportPlanner | None = None,
        narrative_builder: NarrativeBuilder | None = None,
        table_builder: TableBuilder | None = None,
        insight_builder: InsightBuilder | None = None,
    ) -> None:
        """Initialise le builder avec des composants par défaut si besoin.

        :param planner: Planificateur.
        :type planner: ReportPlanner | None
        :param narrative_builder: Narratif.
        :type narrative_builder: NarrativeBuilder | None
        :param table_builder: Tableaux.
        :type table_builder: TableBuilder | None
        :param insight_builder: Insights.
        :type insight_builder: InsightBuilder | None
        """
        self._planner: ReportPlanner = planner if planner is not None else ReportPlanner()
        self._narrative: NarrativeBuilder = (
            narrative_builder if narrative_builder is not None else NarrativeBuilder()
        )
        self._tables: TableBuilder = table_builder if table_builder is not None else TableBuilder()
        self._insights: InsightBuilder = (
            insight_builder if insight_builder is not None else InsightBuilder()
        )

    def build(  # pylint: disable=too-many-locals
        self,
        definition: ReportDefinition,
        context: ReportContext,
    ) -> ReportModel:
        """Construit le modèle complet pour la définition et le contexte donnés.

        :param definition: Gabarit du rapport.
        :type definition: ReportDefinition
        :param context: Période et KPI.
        :type context: ReportContext
        :return: Modèle prêt pour un futur rendu.
        :rtype: ReportModel
        :raises ReportGenerationError: Si aucune section n'est incluse.
        """
        included, decisions = self._planner.plan(definition, context)
        if len(included) == 0:
            raise ReportGenerationError(
                "Aucune section éligible pour ce rapport",
                report_type=definition.report_type,
                details="jeux de KPI insuffisants pour la définition choisie",
            )
        period_start, period_end = context.period_iso_bounds()
        title = definition.title_template.format(
            period_start=period_start,
            period_end=period_end,
        )
        preamble = [self._narrative.lead_paragraph(context, title)]
        decision_by_code = {d.section_code: d for d in decisions}
        built_sections: list[dict[str, object]] = []
        for editorial, _ in included:
            section_code = editorial.section_code
            section_title = editorial.section_title
            dec = decision_by_code[section_code]
            kpis = self._kpis_for_editorial(editorial, context, dec.status)
            narratives = [
                self._narrative.editorial_section_intro(
                    editorial,
                    len(kpis),
                    dec.status,
                ),
            ]
            if editorial.display_rules.show_metric_tables:
                table = self._tables.from_kpi_rows(
                    section_title,
                    kpis,
                    context=context,
                    table_policy=editorial.table_policy,
                )
            else:
                table = {
                    "caption": section_title,
                    "headers": [],
                    "rows": [],
                }
            insight_list = self._insights_for_section(section_code, kpis, context)
            built_sections.append(
                {
                    "section_code": section_code,
                    "title": section_title,
                    "narrative_blocks": narratives,
                    "tables": [table],
                    "insights": insight_list,
                    "eligibility_status": dec.status.value,
                    "eligibility_reason": dec.reason,
                }
            )
        logger.info(
            "ReportModel construit : type=%s, sections=%d",
            definition.report_type,
            len(built_sections),
        )
        return ReportModel(
            report_type=definition.report_type,
            title=title,
            period_start=period_start,
            period_end=period_end,
            preamble_narratives=preamble,
            sections=built_sections,
        )

    @staticmethod
    def _kpis_for_editorial(
        editorial: EditorialSectionDefinition,
        context: ReportContext,
        status: SectionStatus,
    ) -> list[dict[str, object]]:
        """Sélectionne les enregistrements KPI affichés pour une section.

        :param editorial: Section éditoriale courante.
        :type editorial: EditorialSectionDefinition
        :param context: Contexte KPI.
        :type context: ReportContext
        :param status: Statut de planification (dégradé => liste vide).
        :type status: SectionStatus
        :return: Lignes KPI pour tableaux et insights.
        :rtype: list[dict[str, object]]
        """
        if status == SectionStatus.DEGRADED:
            return []
        if editorial.section_code == "weekly_conclusion":
            return []
        prefixes = editorial.visibility_rule.kpi_prefixes
        if not prefixes:
            return context.kpis_matching_prefixes(frozenset())
        return context.kpis_matching_prefixes(prefixes)

    def _insights_for_section(
        self,
        section_code: str,
        kpis: list[dict[str, object]],
        context: ReportContext,
    ) -> list[str]:
        """Sélectionne la stratégie d'insights selon la section.

        :param section_code: Code de section.
        :type section_code: str
        :param kpis: KPI filtrés.
        :type kpis: list[dict[str, object]]
        :param context: Contexte courant.
        :type context: ReportContext
        :return: Liste d'insights.
        :rtype: list[str]
        """
        if section_code in _INSIGHT_TELEPHONY_CODES:
            return self._insights.telephony_balance_insights(
                kpis,
                context=context,
            )
        if section_code in _INSIGHT_CHANNEL_CODES:
            return self._insights.channel_mix_insights(
                kpis,
                context=context,
            )
        return self._insights.generic_numeric_highlights(
            kpis,
            context=context,
        )
