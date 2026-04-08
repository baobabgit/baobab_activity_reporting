"""Contexte partagé pour la rédaction de sections et les insights éditoriaux."""

from __future__ import annotations

from dataclasses import dataclass

from baobab_activity_reporting.domain.results.section_decision import SectionStatus
from baobab_activity_reporting.domain.results.section_eligibility_detail import (
    SectionEligibilityDetail,
)
from baobab_activity_reporting.reporting.editorial.editorial_section_definition import (
    EditorialSectionDefinition,
)
from baobab_activity_reporting.reporting.report_context import ReportContext


@dataclass(frozen=True, slots=True)
class SectionEditorialContext:  # pylint: disable=too-many-instance-attributes
    """Données d'entrée communes aux rédacteurs de narratif et d'insights.

    Sépare la sélection brute (KPI) de la rédaction : les classes de rédaction
    ne lisent pas directement le dépôt ni les writers documentaires.

    :param report_type: Identifiant du type de rapport (ex. ``weekly_activity_by_agent``).
    :param section_code: Code stable de la section.
    :param section_title: Titre affiché.
    :param section_objective: Objectif éditorial (peut être vide).
    :param period_start: Borne début ISO ``YYYY-MM-DD``.
    :param period_end: Borne fin ISO ``YYYY-MM-DD``.
    :param status: Statut d'éligibilité de la section.
    :param kpi_rows: KPI filtrés pour la section courante.
    :param full_kpi_rows: Tous les KPI du contexte (synthèse, filtrage global).
    :param eligibility_detail: Motifs structurés si la planification en fournit.
    """

    report_type: str
    section_code: str
    section_title: str
    section_objective: str
    period_start: str
    period_end: str
    status: SectionStatus
    kpi_rows: tuple[dict[str, object], ...]
    full_kpi_rows: tuple[dict[str, object], ...]
    eligibility_detail: SectionEligibilityDetail | None

    @classmethod
    def from_editorial(  # pylint: disable=too-many-arguments,too-many-positional-arguments
        cls,
        editorial: EditorialSectionDefinition,
        report_type: str,
        period_start: str,
        period_end: str,
        status: SectionStatus,
        kpi_rows: list[dict[str, object]],
        full_context: ReportContext,
        *,
        eligibility_detail: SectionEligibilityDetail | None = None,
    ) -> SectionEditorialContext:
        """Construit un contexte à partir d'une section éditoriale et du rapport.

        :param editorial: Définition de la section.
        :param report_type: Type logique du rapport.
        :param period_start: Date début ISO.
        :param period_end: Date fin ISO.
        :param status: Statut de section.
        :param kpi_rows: KPI déjà filtrés pour cette section.
        :param full_context: Contexte complet (période + tous les KPI).
        :param eligibility_detail: Détail d'éligibilité optionnel.
        :return: Instance figée prête pour les rédacteurs.
        """
        return cls(
            report_type=report_type,
            section_code=editorial.section_code,
            section_title=editorial.section_title,
            section_objective=(editorial.section_objective or "").strip(),
            period_start=period_start,
            period_end=period_end,
            status=status,
            kpi_rows=tuple(dict(r) for r in kpi_rows),
            full_kpi_rows=tuple(dict(r) for r in full_context.kpi_records),
            eligibility_detail=eligibility_detail,
        )
