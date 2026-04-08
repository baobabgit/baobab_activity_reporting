"""Style rédactionnel attendu pour une section de rapport."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class WritingStyle:
    """Décrit le ton et la forme du texte produit pour la section.

    :param tone: Niveau de formalité ou registre (ex. ``professionnel``).
    :type tone: str
    :param perspective: Point de vue rédactionnel (ex. ``tiers``).
    :type perspective: str
    :param length_hint: Consigne de longueur (ex. ``synthetique``).
    :type length_hint: str
    """

    tone: str
    perspective: str
    length_hint: str

    @classmethod
    def default(cls) -> WritingStyle:
        """Style neutre pour rapports d'activité internes.

        :return: Instance par défaut.
        :rtype: WritingStyle
        """
        return cls(
            tone="professionnel",
            perspective="tiers",
            length_hint="synthetique",
        )
