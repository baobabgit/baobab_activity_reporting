"""Module de construction de tableaux structurés."""

from __future__ import annotations

from baobab_activity_reporting.reporting.editorial.table_layout_kind import (
    TableLayoutKind,
)
from baobab_activity_reporting.reporting.editorial.table_policy import TablePolicy
from baobab_activity_reporting.reporting.presentation.kpi_value_presentation_formatter import (
    KpiValuePresentationFormatter,
)
from baobab_activity_reporting.reporting.presentation.section_kpi_table_projector import (
    SectionKpiTableProjector,
)
from baobab_activity_reporting.reporting.presentation.technical_label_sanitizer import (
    TechnicalLabelSanitizer,
)
from baobab_activity_reporting.reporting.report_context import ReportContext

_DEFAULT_MAX_ROWS: int = 8


class TableBuilder:
    """Construit des tableaux métier (sans code KPI ni colonnes techniques).

    Délègue la sélection à :class:`SectionKpiTableProjector` et le formatage des
    valeurs à :class:`KpiValuePresentationFormatter`.

    :Example:
        >>> from baobab_activity_reporting.reporting.table_builder import (
        ...     TableBuilder,
        ... )
        >>> rows = [{"code": "a.b", "label": "Libellé", "value": 1.0, "unit": "u"}]
        >>> t = TableBuilder().from_kpi_rows("cap", rows)
        >>> "Code" in t["headers"]
        False
    """

    def __init__(self) -> None:
        """Initialise projecteur et formateurs réutilisables."""
        self._projector = SectionKpiTableProjector()
        self._value_fmt = KpiValuePresentationFormatter()
        self._labels = TechnicalLabelSanitizer()

    def from_kpi_rows(
        self,
        caption: str,
        kpi_rows: list[dict[str, object]],
        *,
        section_code: str = "",
        context: ReportContext | None = None,
        table_policy: TablePolicy | None = None,
    ) -> dict[str, object]:
        """Assemble un tableau présentable à partir d'enregistrements KPI.

        :param caption: Légende du tableau.
        :type caption: str
        :param kpi_rows: Lignes KPI brutes.
        :type kpi_rows: list[dict[str, object]]
        :param section_code: Code section (informationnel / extensions futures).
        :type section_code: str
        :param context: Contexte optionnel (extensions).
        :type context: ReportContext | None
        :param table_policy: Politique ; défaut : compact limité.
        :type table_policy: TablePolicy | None
        :return: ``caption``, ``headers``, ``rows``, ``skipped``, ``presentation_alerts``.
        :rtype: dict[str, object]
        """
        _ = context
        _ = section_code
        policy = table_policy if table_policy is not None else TablePolicy()
        cap = policy.max_rows if policy.max_rows is not None else _DEFAULT_MAX_ROWS
        projected, alerts = self._projector.project(
            policy.layout_kind,
            kpi_rows,
            max_rows=cap,
        )
        if not projected:
            return {
                "caption": caption,
                "headers": [],
                "rows": [],
                "skipped": True,
                "presentation_alerts": list(alerts),
            }
        headers, body, body_alerts = self._assemble_body(policy.layout_kind, projected)
        merged_alerts = list(alerts) + body_alerts
        return {
            "caption": caption,
            "headers": headers,
            "rows": body,
            "skipped": False,
            "presentation_alerts": merged_alerts,
        }

    def _assemble_body(
        self,
        layout: TableLayoutKind,
        rows: list[dict[str, object]],
    ) -> tuple[list[str], list[list[str]], list[str]]:
        """Construit en-têtes et lignes textuelles.

        :param layout: Mode de présentation.
        :type layout: TableLayoutKind
        :param rows: Lignes déjà projetées.
        :type rows: list[dict[str, object]]
        :return: ``(headers, body, alertes_supplémentaires)``.
        :rtype: tuple[list[str], list[list[str]], list[str]]
        """
        extra: list[str] = []
        if layout == TableLayoutKind.CHANNEL_DISTRIBUTION:
            headers = ["Canal", "Volume"]
            body = []
            bad_channel = False
            for row in rows:
                code = str(row.get("code", ""))
                channel = code.removeprefix("tickets.channel.").removesuffix(".count")
                if not channel.strip():
                    channel = "—"
                    bad_channel = True
                body.append([channel, self._value_fmt.format_value_cell(row)])
            if bad_channel:
                extra.append(
                    "Canal ticket sans libellé exploitable sur au moins une ligne.",
                )
            return headers, body, extra
        if layout == TableLayoutKind.AGENT_VENTILATION:
            headers = ["Agent", "Indicateur", "Valeur"]
            body = []
            for row in rows:
                agent_lbl = SectionKpiTableProjector.agent_label_for_row(row)
                ind = self._indicator_label(row)
                body.append(
                    [agent_lbl, ind, self._value_fmt.format_value_cell(row)],
                )
            return headers, body, extra
        if layout == TableLayoutKind.SITE_VENTILATION:
            headers = ["Site", "Indicateur", "Valeur"]
            body = []
            for row in rows:
                site_lbl = SectionKpiTableProjector.site_label_for_row(row)
                ind = self._indicator_label(row)
                body.append(
                    [site_lbl, ind, self._value_fmt.format_value_cell(row)],
                )
            return headers, body, extra
        headers = ["Indicateur", "Valeur"]
        body = [
            [self._indicator_label(row), self._value_fmt.format_value_cell(row)] for row in rows
        ]
        return headers, body, extra

    def _indicator_label(self, row: dict[str, object]) -> str:
        """Libellé métier pour la colonne indicateur.

        :param row: Ligne KPI.
        :type row: dict[str, object]
        :return: Texte sans code KPI exposé.
        :rtype: str
        """
        label = str(row.get("label", "")).strip()
        if label:
            return self._labels.sanitize(label)
        return self._labels.short_indicator_from_code(str(row.get("code", "")))
