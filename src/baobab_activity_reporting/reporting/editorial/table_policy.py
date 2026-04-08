"""Politique de construction des tableaux pour une section éditoriale."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class TablePolicy:
    """Paramètres de tri, pagination implicite et colonnes pour les tableaux KPI.

    :param max_rows: Limite de lignes affichées (``None`` = illimité).
    :type max_rows: int | None
    :param sort_by_numeric_value_desc: Trier par valeur numérique décroissante.
    :type sort_by_numeric_value_desc: bool
    :param include_site_agent_channel_columns: Inclure colonnes dimensions.
    :type include_site_agent_channel_columns: bool
    """

    max_rows: int | None
    sort_by_numeric_value_desc: bool
    include_site_agent_channel_columns: bool

    @classmethod
    def default(cls) -> TablePolicy:
        """Politique standard alignée sur :class:`TableBuilder`.

        :return: Instance par défaut.
        :rtype: TablePolicy
        """
        return cls(
            max_rows=None,
            sort_by_numeric_value_desc=False,
            include_site_agent_channel_columns=True,
        )
