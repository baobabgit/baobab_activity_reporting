"""Nettoyage des libellés issus des KPI pour l'affichage lecteur."""


class TechnicalLabelSanitizer:
    """Atténue les formulations trop techniques dans les libellés sources."""

    @staticmethod
    def sanitize(label: str, *, max_length: int = 72) -> str:
        """Normalise un libellé pour colonne « Indicateur ».

        :param label: Texte brut (souvent issu du référentiel KPI).
        :type label: str
        :param max_length: Troncature douce si dépassement.
        :type max_length: int
        :return: Libellé nettoyé, une ligne.
        :rtype: str
        """
        text = " ".join(str(label).split())
        if len(text) > max_length:
            return f"{text[: max_length - 1].rstrip()}…"
        return text

    @staticmethod
    def short_indicator_from_code(code: str) -> str:
        """Produit un intitulé court à partir d'un code KPI (sans l'exposer tel quel).

        :param code: Code interne (ex. ``telephony.incoming.count``).
        :type code: str
        :return: Libellé lisible approximatif.
        :rtype: str
        """
        parts = [p for p in str(code).replace("_", ".").split(".") if p]
        if not parts:
            return "Indicateur"
        tail = parts[-1]
        mapping = {
            "count": "volume",
            "sum": "total",
            "avg": "moyenne",
        }
        tail_fr = mapping.get(tail, tail)
        if len(parts) >= 2:
            return f"{parts[-2]} — {tail_fr}"
        return tail_fr
