"""Formatage d'une valeur KPI pour affichage métier dans un tableau."""

from __future__ import annotations

from baobab_activity_reporting.reporting.presentation.business_numeric_rounding import (
    BusinessNumericRounding,
)
from baobab_activity_reporting.reporting.presentation.dimension_anomaly_checker import (
    DimensionAnomalyChecker,
)
from baobab_activity_reporting.reporting.presentation.duration_formatter import (
    DurationFormatter,
)
from baobab_activity_reporting.reporting.presentation.volume_formatter import (
    VolumeFormatter,
)


class KpiValuePresentationFormatter:
    """Choisit le format d'affichage selon le code et l'unité du KPI."""

    def __init__(self) -> None:
        """Instancie les formateurs internes réutilisables."""
        self._duration = DurationFormatter()
        self._volume = VolumeFormatter()

    def format_value_cell(self, row: dict[str, object]) -> str:
        """Produit la cellule « valeur » lisible pour une ligne KPI.

        :param row: Enregistrement avec ``code``, ``value``, ``unit`` optionnel.
        :type row: dict[str, object]
        :return: Texte affichable (durées, volumes, etc.).
        :rtype: str
        """
        if DimensionAnomalyChecker.is_placeholder_value(row.get("value")):
            return "—"
        raw_val = row.get("value")
        try:
            numeric = float(raw_val)  # type: ignore[arg-type]
        except (TypeError, ValueError):
            return "—"

        code = str(row.get("code", ""))
        unit = str(row.get("unit") or "").lower()

        if "duration_seconds" in code or unit == "s":
            return self._duration.format_seconds(numeric)

        if unit in {"appels", "tickets"} or (
            ".count" in code and "channel" not in code and "duration" not in code
        ):
            return self._volume.format_count(numeric)

        if "avg" in code and unit == "s":
            return self._duration.format_seconds(numeric)

        return BusinessNumericRounding.display_float(numeric, decimals=2)
