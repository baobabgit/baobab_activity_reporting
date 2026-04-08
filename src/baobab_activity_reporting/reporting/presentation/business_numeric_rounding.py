"""Arrondis d'affichage pour valeurs métier non entières."""

from __future__ import annotations

import math


class BusinessNumericRounding:
    """Centralise les arrondis d'affichage (hors rendu documentaire)."""

    @staticmethod
    def display_float(value: float, *, decimals: int = 2) -> str:
        """Arrondit un flottant générique pour affichage.

        :param value: Nombre ; non fini → tiret cadratin.
        :type value: float
        :param decimals: Décimales conservées.
        :type decimals: int
        :return: Texte avec virgule décimale.
        :rtype: str
        """
        if not math.isfinite(value):
            return "—"
        rounded = round(value, decimals)
        fmt = f"{{:.{decimals}f}}"
        return fmt.format(rounded).replace(".", ",")
