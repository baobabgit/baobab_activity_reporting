"""Module contenant la décision de section de rapport."""

from enum import Enum


class SectionStatus(Enum):
    """Statut d'inclusion d'une section dans un rapport.

    :cvar INCLUDED: La section est incluse dans le rapport.
    :cvar EXCLUDED: La section est retirée (données insuffisantes).
    :cvar DEGRADED: La section est incluse en mode dégradé.
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
    :param reason: Raison de la décision.
    :type reason: str | None

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
    ) -> None:
        """Initialise la décision de section.

        :param section_code: Code de la section.
        :type section_code: str
        :param status: Statut de la décision.
        :type status: SectionStatus
        :param reason: Raison de la décision.
        :type reason: str | None
        """
        self.section_code: str = section_code
        self.status: SectionStatus = status
        self.reason: str | None = reason

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
            f"reason={self.reason!r})"
        )
