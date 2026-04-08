"""Résultat de l'analyse des signaux « points d'attention »."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class SectionAttentionAssessment:
    """Synthèse des anomalies détectées dans les KPI (sans rendu documentaire).

    :param has_attention_points: Au moins un signal mérite une section vigilance.
    :type has_attention_points: bool
    :param signal_codes: Codes alignés sur :class:`SectionEligibilityCodes`.
    :type signal_codes: frozenset[str]
    :param notes: Détail factuel pour tests et logs.
    :type notes: tuple[str, ...]
    """

    has_attention_points: bool
    signal_codes: frozenset[str]
    notes: tuple[str, ...]
