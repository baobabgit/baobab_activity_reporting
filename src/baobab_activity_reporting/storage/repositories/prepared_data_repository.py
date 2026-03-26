"""Module contenant le repository des données préparées."""

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


class PreparedDataRepository:
    """Repository pour les données nettoyées et normalisées.

    Stocke et restitue les données après passage dans le
    pipeline de standardisation.

    :param session_manager: Gestionnaire de session SQLite.
    :type session_manager: DatabaseSessionManager

    :Example:
        >>> repo = PreparedDataRepository(session_manager)
        >>> repo.save(df, "appels_entrants")
    """

    TABLE_NAME: str = "prepared_data"

    def __init__(self, session_manager: DatabaseSessionManager) -> None:
        """Initialise le repository.

        :param session_manager: Gestionnaire de session.
        :type session_manager: DatabaseSessionManager
        """
        self.session_manager: DatabaseSessionManager = session_manager

    def save(self, dataframe: pd.DataFrame, source_name: str) -> int:
        """Persiste un DataFrame de données préparées.

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
                f"INSERT INTO {self.TABLE_NAME} "  # noqa: S608
                "(source_name, row_data) VALUES (?, ?)",
                rows,
            )
            conn.commit()
        except sqlite3.Error as exc:
            raise PersistenceError(
                "Insertion des données préparées impossible",
                operation="insert",
                details=str(exc),
            ) from exc

        count = len(rows)
        logger.info(
            "%d lignes préparées insérées pour '%s'",
            count,
            source_name,
        )
        return count

    def load(self, source_name: str) -> pd.DataFrame:
        """Charge les données préparées d'une source.

        :param source_name: Nom de la source.
        :type source_name: str
        :return: DataFrame des données préparées.
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
                "Lecture des données préparées impossible",
                operation="select",
                details=str(exc),
            ) from exc

        if not rows:
            return pd.DataFrame()

        records = [json.loads(r[0]) for r in rows]
        result: pd.DataFrame = pd.DataFrame(records)
        logger.info(
            "%d lignes préparées chargées pour '%s'",
            len(result),
            source_name,
        )
        return result

    def count(self, source_name: str) -> int:
        """Compte le nombre de lignes préparées pour une source.

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
        """Supprime les données préparées d'une source.

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
                "Suppression des données préparées impossible",
                operation="delete",
                details=str(exc),
            ) from exc
        count: int = cursor.rowcount
        logger.info(
            "%d lignes préparées supprimées pour '%s'",
            count,
            source_name,
        )
        return count

    def __repr__(self) -> str:
        """Retourne une représentation technique du repository.

        :return: Représentation technique.
        :rtype: str
        """
        return f"PreparedDataRepository(table={self.TABLE_NAME!r})"
