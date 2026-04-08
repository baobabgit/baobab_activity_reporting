"""Module contenant la décision de section de rapport."""

from __future__ import annotations

from enum import Enum

from baobab_activity_reporting.domain.results.section_eligibility_detail import (
    SectionEligibilityDetail,
)


class SectionStatus(Enum):
    """Statut d'inclusion d'une section dans un rapport.

    :cvar INCLUDED: La section est incluse dans le rapport.
    :cvar EXCLUDED: La section est retirée (données insuffisantes).
    :cvar DEGRADED: La section est incluse en mode dégradé ou variante allégée.
    """

    INCLUDED = "included"
    EXCLUDED = "excluded"
    DEGRADED = "degraded"


class SectionDecision:
    """Décision d'inclusion ou d'exclusion d'une section de rapport.

    Encapsule le résultat de l'évaluation d'éligibilité
    d'une section du rapport.

    :param section_code: Code identifiant la section.
    :type section_code: str
    :param status: Statut de la décision.
    :type status: SectionStatus
    :param reason: Raison courte de la décision.
    :type reason: str | None
    :param detail: Motifs structurés et notes de diagnostic.
    :type detail: SectionEligibilityDetail | None

    :Example:
        >>> decision = SectionDecision(
        ...     "telephony_overview",
        ...     SectionStatus.INCLUDED,
        ... )
        >>> print(decision.is_included)
        True
    """

    def __init__(
        self,
        section_code: str,
        status: SectionStatus,
        reason: str | None = None,
        *,
        detail: SectionEligibilityDetail | None = None,
    ) -> None:
        """Initialise la décision de section.

        :param section_code: Code de la section.
        :type section_code: str
        :param status: Statut de la décision.
        :type status: SectionStatus
        :param reason: Raison de la décision.
        :type reason: str | None
        :param detail: Détail d'éligibilité pour tests et logs.
        :type detail: SectionEligibilityDetail | None
        """
        self.section_code: str = section_code
        self.status: SectionStatus = status
        self.reason: str | None = reason
        self.detail: SectionEligibilityDetail | None = detail

    @property
    def is_included(self) -> bool:
        """Indique si la section est incluse dans le rapport.

        :return: ``True`` si le statut est ``INCLUDED`` ou ``DEGRADED``.
        :rtype: bool
        """
        return self.status in (
            SectionStatus.INCLUDED,
            SectionStatus.DEGRADED,
        )

    def __repr__(self) -> str:
        """Retourne une représentation technique de la décision.

        :return: Représentation technique.
        :rtype: str
        """
        return (
            f"SectionDecision("
            f"section_code={self.section_code!r}, "
            f"status={self.status!r}, "
            f"reason={self.reason!r}, "
            f"detail={self.detail!r})"
        )
