"""Module de construction d'insights métier courts."""

from baobab_activity_reporting.reporting.report_context import ReportContext


class InsightBuilder:
    """Déduit quelques phrases d'analyse à partir des valeurs numériques.

    Les règles sont volontairement simples et explicables ; elles ne se
    substituent pas à une couche d'analyse avancée.

    :Example:
        >>> from baobab_activity_reporting.reporting.insight_builder import (
        ...     InsightBuilder,
        ... )
        >>> kpis = [
        ...     {"code": "telephony.incoming.count", "value": 10.0},
        ...     {"code": "telephony.outgoing.count", "value": 5.0},
        ... ]
        >>> outs = InsightBuilder().telephony_balance_insights(kpis)
        >>> len(outs) >= 1
        True
    """

    def telephony_balance_insights(
        self,
        kpi_rows: list[dict[str, object]],
        *,
        context: ReportContext | None = None,
    ) -> list[str]:
        """Compare volumes entrants et sortants lorsque les KPI sont présents.

        :param kpi_rows: Sous-ensemble de KPI téléphonie.
        :type kpi_rows: list[dict[str, object]]
        :param context: Contexte optionnel pour extensions.
        :type context: ReportContext | None
        :return: Liste d'insights (peut être vide).
        :rtype: list[str]
        """
        _ = context
        incoming = self._find_value(kpi_rows, "telephony.incoming.count")
        outgoing = self._find_value(kpi_rows, "telephony.outgoing.count")
        if incoming is None and outgoing is None:
            return []
        insights: list[str] = []
        if incoming is not None and outgoing is not None:
            total = incoming + outgoing
            if total > 0:
                in_pct = 100.0 * incoming / total
                insights.append(
                    f"Les appels entrants représentent environ {in_pct:.1f} % "
                    f"du volume téléphonique ({int(incoming)} entrants, "
                    f"{int(outgoing)} sortants)."
                )
        if incoming is not None:
            insights.append(f"Volume total des appels entrants : {int(incoming)}.")
        if outgoing is not None:
            insights.append(f"Volume total des appels sortants : {int(outgoing)}.")
        return insights

    def channel_mix_insights(
        self,
        kpi_rows: list[dict[str, object]],
        *,
        context: ReportContext | None = None,
    ) -> list[str]:
        """Résume la répartition des volumes par canal ticKet.

        :param kpi_rows: KPI dont le code commence par ``tickets.channel.``.
        :type kpi_rows: list[dict[str, object]]
        :param context: Contexte optionnel.
        :type context: ReportContext | None
        :return: Insights sur les canaux.
        :rtype: list[str]
        """
        _ = context
        pairs: list[tuple[str, float]] = []
        for row in kpi_rows:
            code = str(row.get("code", "")).removeprefix("tickets.channel.").removesuffix(".count")
            if not code:
                code = str(row.get("code", ""))
            val = row.get("value")
            if isinstance(val, (int, float)) and not isinstance(val, bool):
                pairs.append((code, float(val)))
        if not pairs:
            return []
        total = sum(v for _, v in pairs)
        if total <= 0:
            return ["Aucun volume ticket sur les canaux pour cette période."]
        insights: list[str] = []
        for name, val in sorted(pairs, key=lambda x: -x[1]):
            pct = 100.0 * val / total
            insights.append(f"Canal {name} : {pct:.1f} % du volume ({int(val)}).")
        return insights

    def generic_numeric_highlights(
        self,
        kpi_rows: list[dict[str, object]],
        *,
        context: ReportContext | None = None,
    ) -> list[str]:
        """Liste les indicateurs avec valeur numérique sous forme courte.

        :param kpi_rows: Enregistrements KPI de la section.
        :type kpi_rows: list[dict[str, object]]
        :param context: Contexte optionnel.
        :type context: ReportContext | None
        :return: Bullets de synthèse.
        :rtype: list[str]
        """
        _ = context
        lines: list[str] = []
        for row in sorted(kpi_rows, key=lambda r: str(r.get("code", ""))):
            label = str(row.get("label", row.get("code", "")))
            val = row.get("value")
            unit = row.get("unit")
            if isinstance(val, (int, float)) and not isinstance(val, bool):
                u = "" if unit is None else f" {unit}"
                lines.append(f"{label} : {val}{u}.")
        return lines

    @staticmethod
    def _find_value(kpi_rows: list[dict[str, object]], code: str) -> float | None:
        """Retourne la valeur d'un code KPI ou ``None``.

        :param kpi_rows: Lignes source.
        :type kpi_rows: list[dict[str, object]]
        :param code: Code exact recherché.
        :type code: str
        :return: Valeur float ou ``None``.
        :rtype: float | None
        """
        for row in kpi_rows:
            if str(row.get("code", "")) == code:
                val = row.get("value")
                if isinstance(val, (int, float)) and not isinstance(val, bool):
                    return float(val)
        return None
