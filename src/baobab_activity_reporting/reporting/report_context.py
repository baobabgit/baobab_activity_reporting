"""Module du contexte de génération de rapport."""

from baobab_activity_reporting.domain.models.reporting_period import (
    ReportingPeriod,
)


class ReportContext:
    """Porte la période et les KPI disponibles pour construire un rapport.

    Les enregistrements KPI reprennent la forme produite par
    :class:`~baobab_activity_reporting.storage.repositories.kpi_repository.KpiRepository`
    (clés ``code``, ``label``, ``value``, ``unit``, etc.).

    :param reporting_period: Période couverte par le rapport.
    :type reporting_period: ReportingPeriod
    :param kpi_records: Liste de dictionnaires KPI pour la période.
    :type kpi_records: list[dict[str, object]]
    :param locale: Indication de locale pour les libellés (informatif).
    :type locale: str

    :Example:
        >>> from datetime import date
        >>> from baobab_activity_reporting.domain.models.reporting_period import (
        ...     ReportingPeriod,
        ... )
        >>> from baobab_activity_reporting.reporting.report_context import (
        ...     ReportContext,
        ... )
        >>> p = ReportingPeriod(date(2026, 1, 1), date(2026, 1, 31))
        >>> ctx = ReportContext(p, [{"code": "telephony.incoming.count", "value": 1.0}])
        >>> "telephony.incoming.count" in ctx.kpi_codes()
        True
    """

    def __init__(
        self,
        reporting_period: ReportingPeriod,
        kpi_records: list[dict[str, object]],
        *,
        locale: str = "fr_FR",
    ) -> None:
        """Initialise le contexte de génération.

        :param reporting_period: Période du rapport.
        :type reporting_period: ReportingPeriod
        :param kpi_records: KPI disponibles.
        :type kpi_records: list[dict[str, object]]
        :param locale: Locale pour futures extensions de formatage.
        :type locale: str
        """
        self.reporting_period: ReportingPeriod = reporting_period
        self.kpi_records: list[dict[str, object]] = list(kpi_records)
        self.locale: str = locale

    def kpi_codes(self) -> set[str]:
        """Retourne l'ensemble des codes KPI présents.

        :return: Codes normalisés en chaînes.
        :rtype: set[str]
        """
        codes: set[str] = set()
        for row in self.kpi_records:
            raw = row.get("code")
            if raw is not None:
                codes.add(str(raw))
        return codes

    def kpis_matching_prefixes(self, prefixes: frozenset[str]) -> list[dict[str, object]]:
        """Filtre les enregistrements dont ``code`` commence par un préfixe.

        :param prefixes: Préfixes à tester (aucun si ensemble vide).
        :type prefixes: frozenset[str]
        :return: Copie superficielle des lignes concernées.
        :rtype: list[dict[str, object]]
        """
        if not prefixes:
            return list(self.kpi_records)
        result: list[dict[str, object]] = []
        for row in self.kpi_records:
            code = str(row.get("code", ""))
            if any(code.startswith(prefix) for prefix in prefixes):
                result.append(dict(row))
        return result

    def period_iso_bounds(self) -> tuple[str, str]:
        """Bornes ISO ``(début, fin)`` de la période.

        :return: Dates ISO ``YYYY-MM-DD``.
        :rtype: tuple[str, str]
        """
        start = self.reporting_period.start_date.isoformat()
        end = self.reporting_period.end_date.isoformat()
        return start, end

    def __repr__(self) -> str:
        """Représentation technique.

        :return: Représentation.
        :rtype: str
        """
        return f"ReportContext(kpi_count={len(self.kpi_records)}, " f"locale={self.locale!r})"
