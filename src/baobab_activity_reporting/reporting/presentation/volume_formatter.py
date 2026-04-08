"""Formatage métier des volumes (comptages entiers)."""

from __future__ import annotations

import math


class VolumeFormatter:
    """Affiche les volumes comme entiers avec séparateur d'espaces (style français)."""

    @staticmethod
    def format_count(value: float) -> str:
        """Formate un volume entier pour lecture humaine.

        :param value: Nombre à arrondir ; non fini → tiret cadratin.
        :type value: float
        :return: Entier avec espaces comme séparateurs de milliers.
        :rtype: str
        """
        if not math.isfinite(value):
            return "—"
        rounded = int(round(value))
        raw = f"{abs(rounded):,}"
        spaced = raw.replace(",", " ")
        if rounded < 0:
            return f"-{spaced}"
        return spaced
