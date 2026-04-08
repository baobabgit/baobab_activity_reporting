"""Règles d'éligibilité pour les ventilations par agent ou par site."""

from __future__ import annotations

import re
from typing import Literal

from baobab_activity_reporting.domain.results.section_decision import SectionStatus
from baobab_activity_reporting.domain.results.section_eligibility_codes import (
    SectionEligibilityCodes,
)
from baobab_activity_reporting.domain.results.section_eligibility_detail import (
    SectionEligibilityDetail,
)
from baobab_activity_reporting.reporting.report_context import ReportContext

_Dimension = Literal["agent", "site"]


class SectionDimensionalBreakdownEligibilityGate:
    """Exige au moins deux entités distinctes pour une répartition fiable."""

    def __init__(self, dimension: _Dimension) -> None:
        """Fixe la dimension analysée.

        :param dimension: ``agent`` ou ``site``.
        :type dimension: Literal['agent', 'site']
        """
        self._dimension: _Dimension = dimension
        self._pattern: re.Pattern[str] = re.compile(rf"^{dimension}\.([^.]+)\.")

    def evaluate(
        self, context: ReportContext
    ) -> tuple[SectionStatus, str | None, SectionEligibilityDetail]:
        """Décide si la ventilation dimensionnelle est exploitable.

        :param context: KPI disponibles.
        :type context: ReportContext
        :return: Statut, raison et détail.
        :rtype: tuple[SectionStatus, str | None, SectionEligibilityDetail]
        """
        labels: set[str] = set()
        for row in context.kpi_records:
            code = str(row.get("code", ""))
            match = self._pattern.match(code)
            if match:
                labels.add(match.group(1))

        if len(labels) < 2:
            detail = SectionEligibilityDetail(
                codes=frozenset(
                    {SectionEligibilityCodes.EXCLUDED_INSUFFICIENT_BREAKDOWN_DIMENSIONS}
                ),
                notes=(f"dimension={self._dimension!r}, entités_distinctes={len(labels)}.",),
            )
            return (
                SectionStatus.EXCLUDED,
                f"ventilation {self._dimension} insuffisante (moins de deux entités)",
                detail,
            )

        detail = SectionEligibilityDetail(
            codes=frozenset({SectionEligibilityCodes.MIN_DATA_SATISFIED}),
            notes=(f"dimension={self._dimension!r}, entités_distinctes={len(labels)}.",),
        )
        return SectionStatus.INCLUDED, None, detail
