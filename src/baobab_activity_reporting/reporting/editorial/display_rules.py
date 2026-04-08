"""Règles de présentation visuelle et de structuration d'une section."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class DisplayRules:
    """Contrôle l'affichage des blocs (tableaux, mise en avant, compacité).

    :param show_metric_tables: Afficher les tableaux d'indicateurs.
    :type show_metric_tables: bool
    :param collapse_empty_dimensions: Masquer les colonnes entièrement vides.
    :type collapse_empty_dimensions: bool
    :param emphasize_variance: Mettre en avant les écarts (réservé extensions).
    :type emphasize_variance: bool
    """

    show_metric_tables: bool
    collapse_empty_dimensions: bool
    emphasize_variance: bool

    @classmethod
    def default(cls) -> DisplayRules:
        """Règles par défaut pour les rapports d'activité.

        :return: Instance par défaut.
        :rtype: DisplayRules
        """
        return cls(
            show_metric_tables=True,
            collapse_empty_dimensions=True,
            emphasize_variance=False,
        )
