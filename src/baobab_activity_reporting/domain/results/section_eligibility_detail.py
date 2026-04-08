"""Détail structuré d'une décision d'éligibilité de section."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class SectionEligibilityDetail:
    """Motifs et notes pour inclusion, exclusion ou mode dégradé.

    :param codes: Identifiants stables (voir :class:`SectionEligibilityCodes`).
    :type codes: frozenset[str]
    :param notes: Messages lisibles pour le débogage.
    :type notes: tuple[str, ...]
    """

    codes: frozenset[str]
    notes: tuple[str, ...]
