"""Module d'agrégations par site, agent et canal."""

import logging
from typing import Any, Callable, cast

import pandas as pd

from baobab_activity_reporting.exceptions.kpi_computation_error import (
    KpiComputationError,
)

logger = logging.getLogger(__name__)


class ActivityAggregator:
    """Agrège des comptages et sommes par site, agent ou canal.

    Utilise des candidats de noms de colonnes pour rester compatible avec
    les jeux de données normalisés (casse, libellés français).

    :param site_column_candidates: Colonnes possibles pour le site.
    :type site_column_candidates: tuple[str, ...]
    :param agent_column_candidates: Colonnes possibles pour l'agent.
    :type agent_column_candidates: tuple[str, ...]
    :param channel_column_candidates: Colonnes possibles pour le canal.
    :type channel_column_candidates: tuple[str, ...]

    :Example:
        >>> import pandas as pd
        >>> from baobab_activity_reporting.processing.kpi.activity_aggregator import (
        ...     ActivityAggregator,
        ... )
        >>> df = pd.DataFrame({"Site": ["A", "A"], "x": [1, 2]})
        >>> agg = ActivityAggregator()
        >>> s = agg.count_by_site(df)
        >>> int(s.loc["A"])
        2
    """

    def __init__(
        self,
        site_column_candidates: tuple[str, ...] = (
            "Site",
            "site",
            "Service",
            "Site Repartition Ticket",
            "Site Agent Qualification Ticket",
        ),
        agent_column_candidates: tuple[str, ...] = (
            "Agent",
            "agent",
            "Nom de l'agent",
            "Nom Agent Qualification Ticket",
        ),
        channel_column_candidates: tuple[str, ...] = (
            "Canal",
            "canal",
            "Channel",
            "Type Canal Ticket",
        ),
    ) -> None:
        """Initialise l'agrégateur d'activité.

        :param site_column_candidates: Candidats pour la colonne site.
        :type site_column_candidates: tuple[str, ...]
        :param agent_column_candidates: Candidats pour la colonne agent.
        :type agent_column_candidates: tuple[str, ...]
        :param channel_column_candidates: Candidats pour le canal.
        :type channel_column_candidates: tuple[str, ...]
        """
        self.site_column_candidates: tuple[str, ...] = site_column_candidates
        self.agent_column_candidates: tuple[str, ...] = agent_column_candidates
        self.channel_column_candidates: tuple[str, ...] = channel_column_candidates

    def _resolve_column(
        self,
        dataframe: pd.DataFrame,
        candidates: tuple[str, ...],
        role: str,
    ) -> str:
        """Retourne la première colonne présente parmi ``candidates``.

        :param dataframe: Table source.
        :type dataframe: pd.DataFrame
        :param candidates: Liste ordonnée de noms possibles.
        :type candidates: tuple[str, ...]
        :param role: Rôle métier (pour les messages d'erreur).
        :type role: str
        :return: Nom de colonne effectif.
        :rtype: str
        :raises KpiComputationError: Si aucune colonne ne convient.
        """
        cols = set(dataframe.columns.astype(str))
        for name in candidates:
            if name in cols:
                return name
        raise KpiComputationError(
            f"Colonne {role} introuvable pour l'agrégation",
            details=f"candidats={list(candidates)}",
        )

    def resolve_site_column(self, dataframe: pd.DataFrame) -> str:
        """Retourne la colonne site utilisée pour les regroupements.

        :param dataframe: Données contenant un site.
        :type dataframe: pd.DataFrame
        :return: Nom de colonne site.
        :rtype: str
        """
        return self._resolve_column(
            dataframe,
            self.site_column_candidates,
            "site",
        )

    def resolve_site_column_optional(self, dataframe: pd.DataFrame) -> str | None:
        """Retourne une colonne site si présente, sinon ``None``.

        Utile pour les exports sans site (ex. appels sortants téléphoniques).

        :param dataframe: Données éventuellement sans colonne site.
        :type dataframe: pd.DataFrame
        :return: Nom de colonne ou ``None``.
        :rtype: str | None
        """
        cols = set(dataframe.columns.astype(str))
        for name in self.site_column_candidates:
            if name in cols:
                return name
        return None

    def resolve_agent_column(self, dataframe: pd.DataFrame) -> str:
        """Retourne la colonne agent utilisée pour les regroupements.

        :param dataframe: Données contenant un agent.
        :type dataframe: pd.DataFrame
        :return: Nom de colonne agent.
        :rtype: str
        """
        return self._resolve_column(
            dataframe,
            self.agent_column_candidates,
            "agent",
        )

    def resolve_channel_column(self, dataframe: pd.DataFrame) -> str:
        """Retourne la colonne canal utilisée pour les regroupements.

        :param dataframe: Données contenant un canal.
        :type dataframe: pd.DataFrame
        :return: Nom de colonne canal.
        :rtype: str
        """
        return self._resolve_column(
            dataframe,
            self.channel_column_candidates,
            "canal",
        )

    def count_by_site(self, dataframe: pd.DataFrame) -> pd.Series:
        """Compte les lignes par valeur de site.

        :param dataframe: Données non vides avec colonne site.
        :type dataframe: pd.DataFrame
        :return: Série indexée par site.
        :rtype: pd.Series
        """
        site_col = self.resolve_site_column(dataframe)
        grouped = dataframe.groupby(site_col, dropna=False).size()
        logger.info("ActivityAggregator: %d sites distincts", len(grouped))
        return grouped

    def count_by_agent(self, dataframe: pd.DataFrame) -> pd.Series:
        """Compte les lignes par agent.

        :param dataframe: Données non vides avec colonne agent.
        :type dataframe: pd.DataFrame
        :return: Série indexée par agent.
        :rtype: pd.Series
        """
        agent_col = self.resolve_agent_column(dataframe)
        grouped = dataframe.groupby(agent_col, dropna=False).size()
        logger.info("ActivityAggregator: %d agents distincts", len(grouped))
        return grouped

    def count_by_channel(self, dataframe: pd.DataFrame) -> pd.Series:
        """Compte les lignes par canal (ex. tickets).

        :param dataframe: Données non vides avec colonne canal.
        :type dataframe: pd.DataFrame
        :return: Série indexée par canal.
        :rtype: pd.Series
        """
        channel_col = self.resolve_channel_column(dataframe)
        grouped = dataframe.groupby(channel_col, dropna=False).size()
        logger.info("ActivityAggregator: %d canaux distincts", len(grouped))
        return grouped

    def sum_numeric_by_site(
        self,
        dataframe: pd.DataFrame,
        value_column: str,
    ) -> pd.Series:
        """Somme une colonne numérique par site.

        :param dataframe: Données avec site et valeur numérique.
        :type dataframe: pd.DataFrame
        :param value_column: Colonne à sommer.
        :type value_column: str
        :return: Sommes par site.
        :rtype: pd.Series
        """
        site_col = self.resolve_site_column(dataframe)
        values = pd.to_numeric(dataframe[value_column], errors="coerce").fillna(0.0)
        frame = dataframe.assign(_v=values)
        result: pd.Series = frame.groupby(site_col, dropna=False)["_v"].sum()
        return result

    def sum_numeric_by_agent(
        self,
        dataframe: pd.DataFrame,
        value_column: str,
    ) -> pd.Series:
        """Somme une colonne numérique par agent.

        :param dataframe: Données avec agent et valeur numérique.
        :type dataframe: pd.DataFrame
        :param value_column: Colonne à sommer.
        :type value_column: str
        :return: Sommes par agent.
        :rtype: pd.Series
        """
        agent_col = self.resolve_agent_column(dataframe)
        values = pd.to_numeric(dataframe[value_column], errors="coerce").fillna(0.0)
        frame = dataframe.assign(_v=values)
        result: pd.Series = frame.groupby(agent_col, dropna=False)["_v"].sum()
        return result

    def combine_series(
        self,
        left: pd.Series,
        right: pd.Series,
        combine: Callable[[float, float], float],
    ) -> pd.Series:
        """Combine deux séries alignées par index avec une fonction.

        :param left: Première série.
        :type left: pd.Series
        :param right: Deuxième série (même domaine d'index attendu).
        :type right: pd.Series
        :param combine: Fonction ``f(a, b)`` pour fusionner les valeurs.
        :type combine: Callable[[float, float], float]
        :return: Série fusionnée sur l'union des index.
        :rtype: pd.Series
        """
        all_idx = left.index.union(right.index)
        left_r = left.reindex(all_idx, fill_value=0.0)
        right_r = right.reindex(all_idx, fill_value=0.0)

        def _pair(a: object, b: object) -> float:
            return combine(float(cast(Any, a)), float(cast(Any, b)))

        result: pd.Series = left_r.combine(right_r, _pair)
        return result
