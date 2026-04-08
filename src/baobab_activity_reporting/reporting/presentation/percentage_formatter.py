"""Formatage métier des pourcentages."""


class PercentageFormatter:
    """Arrondi cohérent des parts affichées en pourcentage."""

    @staticmethod
    def format_percent(value: float, *, decimals: int = 1) -> str:
        """Formate un pourcentage déjà exprimé sur l'échelle 0–100.

        :param value: Pourcentage (ex. 42.3 pour 42,3 %).
        :type value: float
        :param decimals: Nombre de décimales (défaut 1).
        :type decimals: int
        :return: Chaîne avec virgule décimale et symbole %.
        :rtype: str
        """
        fmt = f"{{:.{decimals}f}}"
        text = fmt.format(value).replace(".", ",")
        return f"{text} %"
