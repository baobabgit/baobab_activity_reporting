"""Formatage métier des durées à partir de secondes."""

from __future__ import annotations

import math


class DurationFormatter:
    """Convertit des durées en secondes vers des libellés lisibles (sans DOCX).

    Règles : secondes brutes si très court ; minutes au-delà d'une minute ;
    heures et minutes pour les durées longues.
    """

    @staticmethod
    def format_seconds(total_seconds: float) -> str:
        """Formate une durée exprimée en secondes.

        :param total_seconds: Durée ; valeurs non finies ou négatives → tiret cadratin.
        :type total_seconds: float
        :return: Chaîne du type ``12 s``, ``3,5 min`` ou ``1 h 5 min``.
        :rtype: str
        """
        if not math.isfinite(total_seconds) or total_seconds < 0:
            return "—"
        if total_seconds < 60:
            return f"{int(round(total_seconds))} s"
        if total_seconds < 3600:
            minutes = total_seconds / 60.0
            if minutes >= 10:
                return f"{round(minutes)} min"
            text = f"{minutes:.1f}".replace(".", ",")
            return f"{text} min"
        hours = int(total_seconds // 3600)
        remainder = total_seconds - hours * 3600
        minutes = int(round(remainder / 60.0))
        if minutes >= 60:
            hours += 1
            minutes = 0
        return f"{hours} h {minutes} min"
