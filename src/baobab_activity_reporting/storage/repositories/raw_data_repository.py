"""Module contenant le repository des données brutes."""

import json
import logging
import sqlite3

import pandas as pd

from baobab_activity_reporting.exceptions.persistence_error import (
    PersistenceError,
)
from baobab_activity_reporting.storage.sqlite.database_session_manager import (
    DatabaseSessionManager,
)

logger = logging.getLogger(__name__)


class RawDataRepository:
    """Repository pour les données brutes extraites.

    Stocke et restitue les données telles qu'elles ont été
    lues par les extracteurs, sans transformation.

    :param session_manager: Gestionnaire de session SQLite.
    :type session_manager: DatabaseSessionManager

    :Example:
        >>> repo = RawDataRepository(session_manager)
        >>> repo.save(df, "appels_entrants")
        >>> df_out = repo.load("appels_entrants")
    """

    TABLE_NAME: str = "raw_data"

    def __init__(self, session_manager: DatabaseSessionManager) -> None:
        """Initialise le repository.

        :param session_manager: Gestionnaire de session.
        :type session_manager: DatabaseSessionManager
        """
        self.session_manager: DatabaseSessionManager = session_manager

    def save(self, dataframe: pd.DataFrame, source_name: str) -> int:
        """Persiste un DataFrame de données brutes.

        Chaque ligne du DataFrame est sérialisée en JSON
        et stockée dans la table ``raw_data``.

        :param dataframe: Données à persister.
        :type dataframe: pd.DataFrame
        :param source_name: Nom de la source.
        :type source_name: str
        :return: Nombre de lignes insérées.
        :rtype: int
        :raises PersistenceError: Si l'insertion échoue.
        """
        conn = self.session_manager.connection
        rows = []
        for _, row in dataframe.iterrows():
            rows.append((source_name, json.dumps(row.to_dict(), default=str)))

        try:
            conn.executemany(
                f"INSERT INTO {self.TABLE_NAME} (source_name, row_data) "  # noqa: S608
                "VALUES (?, ?)",
                rows,
            )
            conn.commit()
        except sqlite3.Error as exc:
            raise PersistenceError(
                "Insertion des données brutes impossible",
                operation="insert",
                details=str(exc),
            ) from exc

        count = len(rows)
        logger.info(
            "%d lignes brutes insérées pour '%s'",
            count,
            source_name,
        )
        return count

    def load(self, source_name: str) -> pd.DataFrame:
        """Charge les données brutes d'une source.

        :param source_name: Nom de la source.
        :type source_name: str
        :return: DataFrame des données brutes.
        :rtype: pd.DataFrame
        :raises PersistenceError: Si la lecture échoue.
        """
        conn = self.session_manager.connection
        try:
            cursor = conn.execute(
                f"SELECT row_data FROM {self.TABLE_NAME} "  # noqa: S608
                "WHERE source_name = ?",
                (source_name,),
            )
            rows = cursor.fetchall()
        except sqlite3.Error as exc:
            raise PersistenceError(
                "Lecture des données brutes impossible",
                operation="select",
                details=str(exc),
            ) from exc

        if not rows:
            return pd.DataFrame()

        records = [json.loads(r[0]) for r in rows]
        result: pd.DataFrame = pd.DataFrame(records)
        logger.info(
            "%d lignes brutes chargées pour '%s'",
            len(result),
            source_name,
        )
        return result

    def count(self, source_name: str) -> int:
        """Compte le nombre de lignes brutes pour une source.

        :param source_name: Nom de la source.
        :type source_name: str
        :return: Nombre de lignes.
        :rtype: int
        """
        conn = self.session_manager.connection
        cursor = conn.execute(
            f"SELECT COUNT(*) FROM {self.TABLE_NAME} "  # noqa: S608
            "WHERE source_name = ?",
            (source_name,),
        )
        result: int = int(cursor.fetchone()[0])
        return result

    def delete(self, source_name: str) -> int:
        """Supprime les données brutes d'une source.

        :param source_name: Nom de la source.
        :type source_name: str
        :return: Nombre de lignes supprimées.
        :rtype: int
        :raises PersistenceError: Si la suppression échoue.
        """
        conn = self.session_manager.connection
        try:
            cursor = conn.execute(
                f"DELETE FROM {self.TABLE_NAME} "  # noqa: S608
                "WHERE source_name = ?",
                (source_name,),
            )
            conn.commit()
        except sqlite3.Error as exc:
            raise PersistenceError(
                "Suppression des données brutes impossible",
                operation="delete",
                details=str(exc),
            ) from exc
        count: int = cursor.rowcount
        logger.info(
            "%d lignes brutes supprimées pour '%s'",
            count,
            source_name,
        )
        return count

    def __repr__(self) -> str:
        """Retourne une représentation technique du repository.

        :return: Représentation technique.
        :rtype: str
        """
        return f"RawDataRepository(table={self.TABLE_NAME!r})"
