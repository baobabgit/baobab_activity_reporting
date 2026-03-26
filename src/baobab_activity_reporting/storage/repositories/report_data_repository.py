"""Module contenant le repository des données de rapport."""

import logging
import sqlite3

from baobab_activity_reporting.exceptions.persistence_error import (
    PersistenceError,
)
from baobab_activity_reporting.storage.sqlite.database_session_manager import (
    DatabaseSessionManager,
)

logger = logging.getLogger(__name__)


class ReportDataRepository:
    """Repository pour les données de rapport générées.

    Stocke et restitue les sections de rapport produites
    par le pipeline de génération.

    :param session_manager: Gestionnaire de session SQLite.
    :type session_manager: DatabaseSessionManager

    :Example:
        >>> repo = ReportDataRepository(session_manager)
        >>> repo.save_section("telephony", "overview", "{...}")
    """

    TABLE_NAME: str = "report_data"

    def __init__(self, session_manager: DatabaseSessionManager) -> None:
        """Initialise le repository.

        :param session_manager: Gestionnaire de session.
        :type session_manager: DatabaseSessionManager
        """
        self.session_manager: DatabaseSessionManager = session_manager

    def save_section(
        self,
        report_type: str,
        section_code: str,
        content: str,
    ) -> None:
        """Persiste une section de rapport.

        :param report_type: Type de rapport.
        :type report_type: str
        :param section_code: Code de la section.
        :type section_code: str
        :param content: Contenu sérialisé de la section.
        :type content: str
        :raises PersistenceError: Si l'insertion échoue.
        """
        conn = self.session_manager.connection
        try:
            conn.execute(
                f"INSERT INTO {self.TABLE_NAME} "  # noqa: S608
                "(report_type, section_code, content) "
                "VALUES (?, ?, ?)",
                (report_type, section_code, content),
            )
            conn.commit()
        except sqlite3.Error as exc:
            raise PersistenceError(
                "Insertion de la section de rapport impossible",
                operation="insert",
                details=str(exc),
            ) from exc
        logger.info(
            "Section '%s' insérée pour le rapport '%s'",
            section_code,
            report_type,
        )

    def load_by_report_type(self, report_type: str) -> list[dict[str, object]]:
        """Charge les sections d'un type de rapport.

        :param report_type: Type de rapport.
        :type report_type: str
        :return: Liste des sections.
        :rtype: list[dict[str, object]]
        :raises PersistenceError: Si la lecture échoue.
        """
        conn = self.session_manager.connection
        try:
            cursor = conn.execute(
                f"SELECT report_type, section_code, "  # noqa: S608
                "content, generated_at "
                f"FROM {self.TABLE_NAME} "
                "WHERE report_type = ?",
                (report_type,),
            )
            rows = cursor.fetchall()
        except sqlite3.Error as exc:
            raise PersistenceError(
                "Lecture des sections de rapport impossible",
                operation="select",
                details=str(exc),
            ) from exc

        results: list[dict[str, object]] = []
        for row in rows:
            results.append(
                {
                    "report_type": row[0],
                    "section_code": row[1],
                    "content": row[2],
                    "generated_at": row[3],
                }
            )
        logger.info(
            "%d sections chargées pour le rapport '%s'",
            len(results),
            report_type,
        )
        return results

    def delete_by_report_type(self, report_type: str) -> int:
        """Supprime les sections d'un type de rapport.

        :param report_type: Type de rapport.
        :type report_type: str
        :return: Nombre de lignes supprimées.
        :rtype: int
        :raises PersistenceError: Si la suppression échoue.
        """
        conn = self.session_manager.connection
        try:
            cursor = conn.execute(
                f"DELETE FROM {self.TABLE_NAME} "  # noqa: S608
                "WHERE report_type = ?",
                (report_type,),
            )
            conn.commit()
        except sqlite3.Error as exc:
            raise PersistenceError(
                "Suppression des sections impossible",
                operation="delete",
                details=str(exc),
            ) from exc
        count: int = cursor.rowcount
        logger.info(
            "%d sections supprimées pour le rapport '%s'",
            count,
            report_type,
        )
        return count

    def __repr__(self) -> str:
        """Retourne une représentation technique du repository.

        :return: Représentation technique.
        :rtype: str
        """
        return f"ReportDataRepository(table={self.TABLE_NAME!r})"
