"""Module de construction de tableaux structurés."""

from baobab_activity_reporting.reporting.editorial.table_policy import TablePolicy
from baobab_activity_reporting.reporting.report_context import ReportContext


class TableBuilder:
    """Construit des tableaux sous forme de dictionnaires sémantiques.

    Chaque tableau comporte les clés ``caption``, ``headers`` et ``rows``.
    Les cellules sont des valeurs primitives (``str``, ``int``, ``float``)
    indépendantes du format de sortie final.

    :Example:
        >>> from baobab_activity_reporting.reporting.table_builder import (
        ...     TableBuilder,
        ... )
        >>> rows = [{"code": "a", "label": "A", "value": 1.0, "unit": "u"}]
        >>> t = TableBuilder().from_kpi_rows("cap", rows)
        >>> t["headers"]
        ['Code', 'Libellé', 'Valeur', 'Unité']
    """

    def from_kpi_rows(
        self,
        caption: str,
        kpi_rows: list[dict[str, object]],
        *,
        context: ReportContext | None = None,
        table_policy: TablePolicy | None = None,
    ) -> dict[str, object]:
        """Assemble un tableau à partir d'enregistrements KPI.

        Colonnes : code, libellé, valeur, unité, dimensions optionnelles
        (site, agent, canal) selon :class:`TablePolicy`.

        :param caption: Légende du tableau.
        :type caption: str
        :param kpi_rows: Lignes KPI (même schéma que le repository).
        :type kpi_rows: list[dict[str, object]]
        :param context: Contexte optionnel (réservé aux extensions).
        :type context: ReportContext | None
        :param table_policy: Politique de tri et colonnes ; défaut si ``None``.
        :type table_policy: TablePolicy | None
        :return: Structure ``caption``, ``headers``, ``rows``.
        :rtype: dict[str, object]
        """
        _ = context
        policy = table_policy if table_policy is not None else TablePolicy.default()
        if policy.include_site_agent_channel_columns:
            headers: list[str] = [
                "Code",
                "Libellé",
                "Valeur",
                "Unité",
                "Site",
                "Agent",
                "Canal",
            ]
            body: list[list[object]] = []
            for row in kpi_rows:
                body.append(
                    [
                        str(row.get("code", "")),
                        str(row.get("label", "")),
                        row.get("value", ""),
                        "" if row.get("unit") is None else str(row.get("unit")),
                        "" if row.get("site") is None else str(row.get("site")),
                        "" if row.get("agent") is None else str(row.get("agent")),
                        "" if row.get("channel") is None else str(row.get("channel")),
                    ],
                )
        else:
            headers = ["Code", "Libellé", "Valeur", "Unité"]
            body = []
            for row in kpi_rows:
                body.append(
                    [
                        str(row.get("code", "")),
                        str(row.get("label", "")),
                        row.get("value", ""),
                        "" if row.get("unit") is None else str(row.get("unit")),
                    ],
                )
        if policy.sort_by_numeric_value_desc and body:

            def _sort_key(row: list[object]) -> float:
                raw = row[2]
                try:
                    if raw is None:
                        return float("-inf")
                    return float(raw)  # type: ignore[arg-type]
                except (TypeError, ValueError):
                    return float("-inf")

            body = sorted(body, key=_sort_key, reverse=True)
        if policy.max_rows is not None:
            body = body[: max(0, policy.max_rows)]
        return {
            "caption": caption,
            "headers": headers,
            "rows": body,
        }
