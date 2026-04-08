"""Sélection et structuration des lignes KPI avant formatage tableau."""

from __future__ import annotations

import math
import re
from typing import Final

from baobab_activity_reporting.reporting.editorial.table_layout_kind import (
    TableLayoutKind,
)
from baobab_activity_reporting.reporting.presentation.dimension_anomaly_checker import (
    DimensionAnomalyChecker,
)


class SectionKpiTableProjector:
    """Réduit les enregistrements KPI à un sous-ensemble pertinent par section.

    Ne réalise aucun rendu DOCX/Markdown : prépare uniquement des lignes sources.
    """

    _KEY_CODE_PRIORITY: Final[tuple[str, ...]] = (
        "telephony.incoming.count",
        "telephony.outgoing.count",
        "telephony.incoming.duration_seconds.sum",
        "telephony.outgoing.duration_seconds.sum",
        "telephony.incoming.duration_seconds.avg",
        "telephony.outgoing.duration_seconds.avg",
    )

    _AGENT_CODE: Final[re.Pattern[str]] = re.compile(r"^agent\.([^.]+)\.")
    _SITE_CODE: Final[re.Pattern[str]] = re.compile(r"^site\.([^.]+)\.")

    def project(
        self,
        layout: TableLayoutKind,
        kpi_rows: list[dict[str, object]],
        *,
        max_rows: int,
    ) -> tuple[list[dict[str, object]], list[str]]:
        """Filtre et ordonne les lignes selon le mode éditorial.

        :param layout: Stratégie de projection.
        :type layout: TableLayoutKind
        :param kpi_rows: Jeu brut issu du contexte.
        :type kpi_rows: list[dict[str, object]]
        :param max_rows: Plafond de lignes (≥ 1).
        :type max_rows: int
        :return: ``(lignes_retenues, alertes_présentation)``.
        :rtype: tuple[list[dict[str, object]], list[str]]
        """
        cap = max(1, max_rows)
        if layout == TableLayoutKind.KEY_FIGURES:
            return self._key_figures(kpi_rows, cap)
        if layout == TableLayoutKind.CHANNEL_DISTRIBUTION:
            return self._channels(kpi_rows, cap)
        if layout == TableLayoutKind.AGENT_VENTILATION:
            return self._dimension_rows(kpi_rows, cap, "agent", self._AGENT_CODE)
        if layout == TableLayoutKind.SITE_VENTILATION:
            return self._dimension_rows(kpi_rows, cap, "site", self._SITE_CODE)
        return self._compact_metrics(kpi_rows, cap)

    def _key_figures(
        self,
        rows: list[dict[str, object]],
        cap: int,
    ) -> tuple[list[dict[str, object]], list[str]]:
        by_code = {str(r.get("code", "")): r for r in rows if r.get("code")}
        ordered: list[dict[str, object]] = []
        for code in self._KEY_CODE_PRIORITY:
            if code in by_code:
                ordered.append(by_code[code])
            if len(ordered) >= cap:
                return ordered, []
        for row in sorted(rows, key=self._sort_strength, reverse=True):
            if row in ordered:
                continue
            ordered.append(row)
            if len(ordered) >= cap:
                break
        return ordered, []

    def _channels(
        self,
        rows: list[dict[str, object]],
        cap: int,
    ) -> tuple[list[dict[str, object]], list[str]]:
        filtered = [
            r
            for r in rows
            if str(r.get("code", "")).startswith("tickets.channel.")
            and str(r.get("code", "")).endswith(".count")
        ]
        filtered.sort(key=self._sort_strength, reverse=True)
        return filtered[:cap], []

    def _dimension_rows(
        self,
        rows: list[dict[str, object]],
        cap: int,
        dim_name: str,
        pattern: re.Pattern[str],
    ) -> tuple[list[dict[str, object]], list[str]]:
        alerts: list[str] = []
        scoped = [r for r in rows if pattern.match(str(r.get("code", "")))]
        scoped.sort(key=self._sort_strength, reverse=True)
        chosen = scoped[:cap]
        key = "agent" if dim_name == "agent" else "site"
        for row in chosen:
            _, bad = DimensionAnomalyChecker.normalize_dimension(row.get(key))
            if bad:
                alerts.append(
                    f"Dimension « {dim_name} » absente ou non fiable sur au moins une ligne "
                    "(affichage complété à partir du regroupement métier).",
                )
                break
        return chosen, alerts

    def _compact_metrics(
        self,
        rows: list[dict[str, object]],
        cap: int,
    ) -> tuple[list[dict[str, object]], list[str]]:
        sorted_rows = sorted(rows, key=self._sort_strength, reverse=True)
        return sorted_rows[:cap], []

    @classmethod
    def agent_label_for_row(cls, row: dict[str, object]) -> str:
        """Libellé agent pour affichage (champ métier ou extrait du regroupement).

        :param row: Ligne KPI.
        :type row: dict[str, object]
        :return: Texte affiché en colonne Agent.
        :rtype: str
        """
        text, bad = DimensionAnomalyChecker.normalize_dimension(row.get("agent"))
        if not bad:
            return text
        match = cls._AGENT_CODE.match(str(row.get("code", "")))
        return match.group(1) if match else "—"

    @classmethod
    def site_label_for_row(cls, row: dict[str, object]) -> str:
        """Libellé site pour affichage.

        :param row: Ligne KPI.
        :type row: dict[str, object]
        :return: Texte affiché en colonne Site.
        :rtype: str
        """
        text, bad = DimensionAnomalyChecker.normalize_dimension(row.get("site"))
        if not bad:
            return text
        match = cls._SITE_CODE.match(str(row.get("code", "")))
        return match.group(1) if match else "—"

    @staticmethod
    def _sort_strength(row: dict[str, object]) -> float:
        raw = row.get("value")
        try:
            x = float(raw)  # type: ignore[arg-type]
        except (TypeError, ValueError):
            return float("-inf")
        if not math.isfinite(x):
            return float("-inf")
        return abs(x)
