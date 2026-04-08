"""Règle de visibilité et de retrait d'une section selon les données KPI."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class SectionVisibilityRule:
    """Détermine quand une section est incluse, exclue ou dégradée.

    Si ``kpi_prefixes`` est vide, la section est toujours éligible sur la
    base des données (équivalent « pas de porte logique »).

    Si les préfixes sont non vides et qu'aucun KPI ne correspond :

    * ``mandatory_in_report`` vrai : la section reste avec statut dégradé.
    * sinon : la section est exclue du plan.

    :param kpi_prefixes: Préfixes de codes KPI requis pour un mode nominal.
    :type kpi_prefixes: frozenset[str]
    :param mandatory_in_report: Conserver la section même sans KPI (dégradé).
    :type mandatory_in_report: bool
    """

    kpi_prefixes: frozenset[str]
    mandatory_in_report: bool

    @classmethod
    def from_prefixes(
        cls,
        prefixes: frozenset[str],
        *,
        mandatory_in_report: bool = False,
    ) -> SectionVisibilityRule:
        """Fabrique une règle à partir d'un ensemble de préfixes.

        :param prefixes: Préfixes KPI (peut être vide).
        :type prefixes: frozenset[str]
        :param mandatory_in_report: Section obligatoire dans le rapport.
        :type mandatory_in_report: bool
        :return: Règle de visibilité.
        :rtype: SectionVisibilityRule
        """
        return cls(
            kpi_prefixes=prefixes,
            mandatory_in_report=mandatory_in_report,
        )
