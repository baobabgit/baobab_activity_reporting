"""Politique de construction des tableaux pour une section éditoriale."""

from __future__ import annotations

from dataclasses import dataclass

from baobab_activity_reporting.reporting.editorial.table_layout_kind import (
    TableLayoutKind,
)


@dataclass(frozen=True, slots=True)
class TablePolicy:
    """Paramètres de projection, limite de lignes et mode tableau métier.

    Les colonnes techniques (code KPI, etc.) ne sont plus produites par le
    :class:`~baobab_activity_reporting.reporting.table_builder.TableBuilder` :
    ``include_site_agent_channel_columns`` est conservé pour compatibilité mais
    ignoré pour le rendu présenté.

    :param max_rows: Limite de lignes ; ``None`` utilise la limite par défaut du builder.
    :type max_rows: int | None
    :param sort_by_numeric_value_desc: Réservé (tri appliqué dans le projecteur).
    :type sort_by_numeric_value_desc: bool
    :param include_site_agent_channel_columns: Compatibilité ; non utilisé pour la présentation.
    :type include_site_agent_channel_columns: bool
    :param layout_kind: Stratégie de sélection des lignes (chiffres clés, canaux, etc.).
    :type layout_kind: TableLayoutKind
    """

    max_rows: int | None = 8
    sort_by_numeric_value_desc: bool = True
    include_site_agent_channel_columns: bool = False
    layout_kind: TableLayoutKind = TableLayoutKind.COMPACT_METRICS

    @classmethod
    def default(cls) -> TablePolicy:
        """Politique pour synthèse : chiffres clés courts.

        :return: Instance par défaut.
        :rtype: TablePolicy
        """
        return cls(
            max_rows=6,
            sort_by_numeric_value_desc=True,
            include_site_agent_channel_columns=False,
            layout_kind=TableLayoutKind.KEY_FIGURES,
        )
