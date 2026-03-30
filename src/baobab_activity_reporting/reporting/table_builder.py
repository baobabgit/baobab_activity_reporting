"""Module de construction de tableaux structurés."""

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
    ) -> dict[str, object]:
        """Assemble un tableau à partir d'enregistrements KPI.

        Colonnes : code, libellé, valeur, unité, dimensions optionnelles
        (site, agent, canal).

        :param caption: Légende du tableau.
        :type caption: str
        :param kpi_rows: Lignes KPI (même schéma que le repository).
        :type kpi_rows: list[dict[str, object]]
        :param context: Contexte optionnel (réservé aux extensions).
        :type context: ReportContext | None
        :return: Structure ``caption``, ``headers``, ``rows``.
        :rtype: dict[str, object]
        """
        _ = context
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
                ]
            )
        return {
            "caption": caption,
            "headers": headers,
            "rows": body,
        }
