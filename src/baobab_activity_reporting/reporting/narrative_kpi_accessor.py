"""Sélection et agrégations KPI pour la couche rédactionnelle (hors rendu DOCX)."""

from __future__ import annotations

import math
from collections import defaultdict
from typing import Sequence


class NarrativeKpiAccessor:
    """Expose des vues métier sur des enregistrements KPI bruts.

    Responsabilité limitée à la **sélection** et au **regroupement** de valeurs
    numériques ; aucune phrase rédigée ni sortie documentaire.
    """

    @staticmethod
    def numeric_for_code(
        kpi_rows: Sequence[dict[str, object]],
        code: str,
    ) -> float | None:
        """Retourne la valeur numérique pour un code KPI exact.

        :param kpi_rows: Lignes KPI.
        :param code: Code recherché.
        :return: Valeur finie ou ``None``.
        """
        for row in kpi_rows:
            if str(row.get("code", "")) != code:
                continue
            val = row.get("value")
            if isinstance(val, (int, float)) and not isinstance(val, bool):
                fval = float(val)
                if math.isfinite(fval):
                    return fval
        return None

    @staticmethod
    def is_global_telephony_code(code: str) -> bool:
        """Indique si le code décrit la téléphonie globale (hors agent/site).

        :param code: Code KPI.
        :return: ``True`` si agrégat téléphonie global.
        """
        if not code.startswith("telephony."):
            return False
        if ".agent." in code or code.startswith("agent."):
            return False
        if ".site." in code or code.startswith("site."):
            return False
        return True

    @staticmethod
    def filter_global_telephony(
        kpi_rows: Sequence[dict[str, object]],
    ) -> list[dict[str, object]]:
        """Sous-ensemble des KPI téléphonie globaux.

        :param kpi_rows: Lignes source.
        :return: Copie superficielle des lignes concernées.
        """
        return [
            dict(r)
            for r in kpi_rows
            if NarrativeKpiAccessor.is_global_telephony_code(str(r.get("code", "")))
        ]

    @staticmethod
    def filter_ticket_channels(
        kpi_rows: Sequence[dict[str, object]],
    ) -> list[dict[str, object]]:
        """KPI de volume par canal ticket (préfixe ``tickets.channel.``).

        :param kpi_rows: Lignes source.
        :return: Lignes concernées.
        """
        return [
            dict(r)
            for r in kpi_rows
            if str(r.get("code", "")).startswith("tickets.channel.")
            and str(r.get("code", "")).endswith(".count")
        ]

    @staticmethod
    def channel_label_and_volume(
        row: dict[str, object],
    ) -> tuple[str, float] | None:
        """Libellé métier et volume pour une ligne canal ticket.

        :param row: Ligne KPI.
        :return: Couple (libellé, volume) ou ``None``.
        """
        code = str(row.get("code", ""))
        if not code.startswith("tickets.channel.") or not code.endswith(".count"):
            return None
        inner = code.removeprefix("tickets.channel.").removesuffix(".count")
        label = str(row.get("label", "") or inner or "Canal").strip()
        val = row.get("value")
        if not isinstance(val, (int, float)) or isinstance(val, bool):
            return None
        volume = float(val)
        if volume < 0:
            return None
        return label, volume

    @staticmethod
    def channel_volumes_sorted(
        kpi_rows: Sequence[dict[str, object]],
    ) -> list[tuple[str, float]]:
        """Volumes par canal, tri décroissant.

        :param kpi_rows: Lignes KPI.
        :return: Liste ``(libellé, volume)``.
        """
        pairs: list[tuple[str, float]] = []
        for row in kpi_rows:
            parsed = NarrativeKpiAccessor.channel_label_and_volume(dict(row))
            if parsed is not None:
                pairs.append(parsed)
        return sorted(pairs, key=lambda x: -x[1])

    @staticmethod
    def incoming_outgoing_counts(
        kpi_rows: Sequence[dict[str, object]],
    ) -> tuple[float | None, float | None]:
        """Compteurs appels entrants et sortants globaux.

        :param kpi_rows: Lignes KPI (souvent filtrées téléphonie globale).
        :return: ``(entrants, sortants)`` avec ``None`` si absent.
        """
        inc = NarrativeKpiAccessor.numeric_for_code(
            kpi_rows,
            "telephony.incoming.count",
        )
        out = NarrativeKpiAccessor.numeric_for_code(
            kpi_rows,
            "telephony.outgoing.count",
        )
        return inc, out

    @staticmethod
    def dimension_totals(
        kpi_rows: Sequence[dict[str, object]],
        dimension_prefix: str,
    ) -> list[tuple[str, float]]:
        """Somme toutes les valeurs numériques par entité ``agent.X`` ou ``site.X``.

        :param kpi_rows: Lignes KPI.
        :param dimension_prefix: ``agent.`` ou ``site.``.
        :return: ``(clé_dimension, total)`` trié par total décroissant.
        """
        buckets: defaultdict[str, float] = defaultdict(float)
        prefix = dimension_prefix
        for row in kpi_rows:
            code = str(row.get("code", ""))
            if not code.startswith(prefix):
                continue
            rest = code[len(prefix) :]
            dot = rest.find(".")
            if dot <= 0:
                continue
            key = rest[:dot]
            val = row.get("value")
            if isinstance(val, (int, float)) and not isinstance(val, bool):
                fval = float(val)
                if math.isfinite(fval):
                    buckets[key] += fval
        return sorted(buckets.items(), key=lambda x: -x[1])
