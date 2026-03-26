"""Module contenant le gestionnaire de session SQLite."""

import logging
import sqlite3
from pathlib import Path

from baobab_activity_reporting.exceptions.persistence_error import (
    PersistenceError,
)

logger = logging.getLogger(__name__)

_RAW_SCHEMA = """
CREATE TABLE IF NOT EXISTS raw_data (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    source_name TEXT NOT NULL,
    ingested_at TEXT NOT NULL DEFAULT (datetime('now')),
    row_data TEXT NOT NULL
);
"""

_PREPARED_SCHEMA = """
CREATE TABLE IF NOT EXISTS prepared_data (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    source_name TEXT NOT NULL,
    prepared_at TEXT NOT NULL DEFAULT (datetime('now')),
    row_data TEXT NOT NULL
);
"""

_KPI_SCHEMA = """
CREATE TABLE IF NOT EXISTS kpi_data (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    code TEXT NOT NULL,
    label TEXT NOT NULL,
    value REAL NOT NULL,
    unit TEXT,
    period_start TEXT,
    period_end TEXT,
    computed_at TEXT NOT NULL DEFAULT (datetime('now'))
);
"""

_REPORT_SCHEMA = """
CREATE TABLE IF NOT EXISTS report_data (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    report_type TEXT NOT NULL,
    section_code TEXT NOT NULL,
    content TEXT NOT NULL,
    generated_at TEXT NOT NULL DEFAULT (datetime('now'))
);
"""

_ALL_SCHEMAS = [_RAW_SCHEMA, _PREPARED_SCHEMA, _KPI_SCHEMA, _REPORT_SCHEMA]


class DatabaseSessionManager:
    """Gestionnaire de connexion et de session SQLite.

    Centralise la création de la connexion, l'initialisation
    du schéma et la fermeture propre de la base de données.

    :param db_path: Chemin vers le fichier SQLite.
        Utiliser ``":memory:"`` pour une base en mémoire.
    :type db_path: str

    :Example:
        >>> manager = DatabaseSessionManager(":memory:")
        >>> conn = manager.connection
        >>> manager.close()
    """

    def __init__(self, db_path: str) -> None:
        """Initialise le gestionnaire de session.

        :param db_path: Chemin vers le fichier SQLite.
        :type db_path: str
        :raises PersistenceError: Si la connexion échoue.
        """
        self.db_path: str = db_path
        self._connection: sqlite3.Connection | None = None
        self._connect()
        self._initialize_schema()

    def _connect(self) -> None:
        """Établit la connexion à la base SQLite.

        :raises PersistenceError: Si la connexion échoue.
        """
        try:
            self._connection = sqlite3.connect(self.db_path)
            self._connection.execute("PRAGMA journal_mode=WAL;")
            logger.info("Connexion SQLite établie : %s", self.db_path)
        except sqlite3.Error as exc:
            raise PersistenceError(
                "Connexion SQLite impossible",
                operation="connect",
                details=str(exc),
            ) from exc

    def _initialize_schema(self) -> None:
        """Crée les tables si elles n'existent pas.

        :raises PersistenceError: Si la création échoue.
        """
        conn = self.connection
        try:
            cursor = conn.cursor()
            for ddl in _ALL_SCHEMAS:
                cursor.execute(ddl)
            conn.commit()
            logger.info("Schéma SQLite initialisé")
        except sqlite3.Error as exc:
            raise PersistenceError(
                "Initialisation du schéma impossible",
                operation="create_tables",
                details=str(exc),
            ) from exc

    @property
    def connection(self) -> sqlite3.Connection:
        """Retourne la connexion SQLite active.

        :return: Connexion SQLite.
        :rtype: sqlite3.Connection
        :raises PersistenceError: Si la connexion est fermée.
        """
        if self._connection is None:
            raise PersistenceError(
                "Connexion SQLite fermée",
                operation="get_connection",
            )
        return self._connection

    def close(self) -> None:
        """Ferme la connexion SQLite.

        :raises PersistenceError: Si la fermeture échoue.
        """
        if self._connection is not None:
            try:
                self._connection.close()
                logger.info("Connexion SQLite fermée : %s", self.db_path)
            except sqlite3.Error as exc:
                raise PersistenceError(
                    "Fermeture de la connexion impossible",
                    operation="close",
                    details=str(exc),
                ) from exc
            finally:
                self._connection = None

    @property
    def is_open(self) -> bool:
        """Indique si la connexion est ouverte.

        :return: ``True`` si la connexion est active.
        :rtype: bool
        """
        return self._connection is not None

    def file_exists(self) -> bool:
        """Vérifie si le fichier de base de données existe sur disque.

        :return: ``True`` si le fichier existe (toujours ``False``
            pour ``:memory:``).
        :rtype: bool
        """
        if self.db_path == ":memory:":
            return False
        return Path(self.db_path).exists()

    def __repr__(self) -> str:
        """Retourne une représentation technique du gestionnaire.

        :return: Représentation technique.
        :rtype: str
        """
        return f"DatabaseSessionManager(" f"db_path={self.db_path!r}, " f"is_open={self.is_open!r})"
