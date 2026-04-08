"""Détection des dimensions ou valeurs placeholders pour la présentation."""


class DimensionAnomalyChecker:
    """Identifie site / agent / canal vides ou non fiables pour le rendu métier."""

    _PLACEHOLDERS: frozenset[str] = frozenset(
        {
            "",
            "—",
            "-",
            "nan",
            "none",
            "null",
            "na",
            "n/a",
            "inconnu",
            "?",
        },
    )

    @classmethod
    def normalize_dimension(cls, raw: object) -> tuple[str, bool]:
        """Retourne le texte affiché et un indicateur d'anomalie.

        :param raw: Valeur dimension (site, agent, canal).
        :type raw: object
        :return: ``(texte, anomalie)`` ; anomalie vraie si donnée manquante.
        :rtype: tuple[str, bool]
        """
        if raw is None:
            return "—", True
        text = str(raw).strip()
        if text.lower() in cls._PLACEHOLDERS:
            return "—", True
        return text, False

    @staticmethod
    def is_placeholder_value(raw: object) -> bool:
        """Indique si une valeur brute est considérée comme non porteuse de sens.

        :param raw: Champ ``value`` ou équivalent.
        :type raw: object
        :return: ``True`` si la valeur doit être traitée comme absente.
        :rtype: bool
        """
        if raw is None:
            return True
        if isinstance(raw, str):
            return raw.strip() == "" or raw.strip() in ("—", "-", "nan")
        return False
