"""Modes de projection des tableaux par section éditoriale."""

from enum import Enum


class TableLayoutKind(str, Enum):
    """Détermine quels KPI sont retenus et la forme du tableau.

    :cvar KEY_FIGURES: Quelques indicateurs globaux prioritaires (téléphonie, etc.).
    :cvar CHANNEL_DISTRIBUTION: Répartition par canal ticket (volumes courts).
    :cvar AGENT_VENTILATION: Lignes liées aux agents, colonnes Agent / Indicateur / Valeur.
    :cvar SITE_VENTILATION: Idem pour les sites.
    :cvar COMPACT_METRICS: Top valeurs par libellé, deux colonnes Indicateur / Valeur.
    """

    KEY_FIGURES = "key_figures"
    CHANNEL_DISTRIBUTION = "channel_distribution"
    AGENT_VENTILATION = "agent_ventilation"
    SITE_VENTILATION = "site_ventilation"
    COMPACT_METRICS = "compact_metrics"
