"""Évaluation des valeurs numériques portées par les enregistrements KPI."""

from __future__ import annotations

import math

from baobab_activity_reporting.reporting.report_context import ReportContext


class KpiValueAssessor:
    """Interprète les champs ``value`` des lignes KPI du contexte.

    Aucun rendu documentaire : uniquement des contrôles de cohérence numérique.
    """

    @staticmethod
    def numeric_for_code(context: ReportContext, code: str) -> float | None:
        """Retourne la valeur numérique finie pour le premier code KPI exact.

        :param context: Contexte courant.
        :type context: ReportContext
        :param code: Code KPI attendu.
        :type code: str
        :return: Flottant fini ou ``None`` si absent ou non fiable.
        :rtype: float | None
        """
        for row in context.kpi_records:
            raw_code = row.get("code")
            if raw_code is None or str(raw_code) != code:
                continue
            return KpiValueAssessor.finite_number(row.get("value"))
        return None

    @staticmethod
    def finite_number(raw: object) -> float | None:
        """Convertit une valeur brute en flottant fini si possible.

        :param raw: Valeur issue du stockage KPI.
        :type raw: object
        :return: Nombre fini ou ``None``.
        :rtype: float | None
        """
        if raw is None or isinstance(raw, bool):
            return None
        if isinstance(raw, (int, float)):
            val = float(raw)
            return val if math.isfinite(val) else None
        try:
            val = float(str(raw).strip().replace(",", "."))
        except (TypeError, ValueError):
            return None
        return val if math.isfinite(val) else None

    @staticmethod
    def sum_channel_ticket_counts(context: ReportContext) -> tuple[float, bool]:
        """Somme les volumes ``tickets.channel.*.count`` et signale l'invalidité.

        :param context: Contexte KPI.
        :type context: ReportContext
        :return: ``(somme, fiable)`` ; ``fiable`` faux si une ligne est invalide.
        :rtype: tuple[float, bool]
        """
        total = 0.0
        for row in context.kpi_records:
            code = str(row.get("code", ""))
            if not code.startswith("tickets.channel.") or not code.endswith(".count"):
                continue
            parsed = KpiValueAssessor.finite_number(row.get("value"))
            if parsed is None:
                return 0.0, False
            if parsed < 0:
                return 0.0, False
            total += parsed
        return total, True
