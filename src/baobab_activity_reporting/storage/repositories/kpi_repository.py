"""Module contenant le repository des KPI."""

import logging
import sqlite3

from baobab_activity_reporting.exceptions.persistence_error import (
    PersistenceError,
)
from baobab_activity_reporting.storage.sqlite.database_session_manager import (
    DatabaseSessionManager,
)

logger = logging.getLogger(__name__)


class KpiRepository:
    """Repository pour les indicateurs clés calculés.

    Stocke et restitue les KPI sous forme de tuples
    structurés (code, label, value, unit, period).

    :param session_manager: Gestionnaire de session SQLite.
    :type session_manager: DatabaseSessionManager

    :Example:
        >>> repo = KpiRepository(session_manager)
        >>> repo.save_kpi("nb_appels", "Nombre d'appels", 142.0)
    """

    TABLE_NAME: str = "kpi_data"

    def __init__(self, session_manager: DatabaseSessionManager) -> None:
        """Initialise le repository.

        :param session_manager: Gestionnaire de session.
        :type session_manager: DatabaseSessionManager
        """
        self.session_manager: DatabaseSessionManager = session_manager

    def save_kpi(  # pylint: disable=too-many-arguments,too-many-positional-arguments
        self,
        code: str,
        label: str,
        value: float,
        unit: str | None = None,
        period_start: str | None = None,
        period_end: str | None = None,
        site: str | None = None,
        agent: str | None = None,
        channel: str | None = None,
    ) -> None:
        """Persiste un indicateur calculé.

        :param code: Code du KPI.
        :type code: str
        :param label: Libellé du KPI.
        :type label: str
        :param value: Valeur numérique.
        :type value: float
        :param unit: Unité de mesure.
        :type unit: str | None
        :param period_start: Début de la période (ISO 8601).
        :type period_start: str | None
        :param period_end: Fin de la période (ISO 8601).
        :type period_end: str | None
        :param site: Site pour les agrégations dimensionnelles.
        :type site: str | None
        :param agent: Agent pour les agrégations dimensionnelles.
        :type agent: str | None
        :param channel: Canal pour les agrégations dimensionnelles.
        :type channel: str | None
        :raises PersistenceError: Si l'insertion échoue.
        """
        conn = self.session_manager.connection
        try:
            conn.execute(
                f"INSERT INTO {self.TABLE_NAME} "  # noqa: S608
                "(code, label, value, unit, period_start, period_end, "
                "site, agent, channel) "
                "VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
                (
                    code,
                    label,
                    value,
                    unit,
                    period_start,
                    period_end,
                    site,
                    agent,
                    channel,
                ),
            )
            conn.commit()
        except sqlite3.Error as exc:
            raise PersistenceError(
                "Insertion du KPI impossible",
                operation="insert",
                details=str(exc),
            ) from exc
        logger.info("KPI '%s' inséré (valeur=%s)", code, value)

    def load_by_code(self, code: str) -> list[dict[str, object]]:
        """Charge les KPI par code.

        :param code: Code du KPI recherché.
        :type code: str
        :return: Liste de dictionnaires représentant les KPI.
        :rtype: list[dict[str, object]]
        :raises PersistenceError: Si la lecture échoue.
        """
        conn = self.session_manager.connection
        try:
            cursor = conn.execute(
                f"SELECT code, label, value, unit, "  # noqa: S608
                "period_start, period_end, site, agent, channel, computed_at "
                f"FROM {self.TABLE_NAME} WHERE code = ?",
                (code,),
            )
            rows = cursor.fetchall()
        except sqlite3.Error as exc:
            raise PersistenceError(
                "Lecture des KPI impossible",
                operation="select",
                details=str(exc),
            ) from exc

        results: list[dict[str, object]] = []
        for row in rows:
            results.append(
                {
                    "code": row[0],
                    "label": row[1],
                    "value": row[2],
                    "unit": row[3],
                    "period_start": row[4],
                    "period_end": row[5],
                    "site": row[6],
                    "agent": row[7],
                    "channel": row[8],
                    "computed_at": row[9],
                }
            )
        logger.info(
            "%d KPI chargés pour le code '%s'",
            len(results),
            code,
        )
        return results

    def load_all(self) -> list[dict[str, object]]:
        """Charge tous les KPI.

        :return: Liste de dictionnaires représentant les KPI.
        :rtype: list[dict[str, object]]
        :raises PersistenceError: Si la lecture échoue.
        """
        conn = self.session_manager.connection
        try:
            cursor = conn.execute(
                f"SELECT code, label, value, unit, "  # noqa: S608
                "period_start, period_end, site, agent, channel, computed_at "
                f"FROM {self.TABLE_NAME}",
            )
            rows = cursor.fetchall()
        except sqlite3.Error as exc:
            raise PersistenceError(
                "Lecture de tous les KPI impossible",
                operation="select",
                details=str(exc),
            ) from exc

        results: list[dict[str, object]] = []
        for row in rows:
            results.append(
                {
                    "code": row[0],
                    "label": row[1],
                    "value": row[2],
                    "unit": row[3],
                    "period_start": row[4],
                    "period_end": row[5],
                    "site": row[6],
                    "agent": row[7],
                    "channel": row[8],
                    "computed_at": row[9],
                }
            )
        logger.info("%d KPI chargés au total", len(results))
        return results

    def load_for_period(
        self,
        period_start: str,
        period_end: str,
    ) -> list[dict[str, object]]:
        """Charge les KPI dont la période correspond aux bornes données.

        Filtre sur ``period_start`` et ``period_end`` tels que persistés
        par le pipeline de calcul (dates ISO).

        :param period_start: Début de période (ISO 8601 date).
        :type period_start: str
        :param period_end: Fin de période (ISO 8601 date).
        :type period_end: str
        :return: Enregistrements KPI de la période.
        :rtype: list[dict[str, object]]
        :raises PersistenceError: Si la lecture échoue.
        """
        conn = self.session_manager.connection
        try:
            cursor = conn.execute(
                f"SELECT code, label, value, unit, "  # noqa: S608
                "period_start, period_end, site, agent, channel, computed_at "
                f"FROM {self.TABLE_NAME} "
                "WHERE period_start = ? AND period_end = ?",
                (period_start, period_end),
            )
            rows = cursor.fetchall()
        except sqlite3.Error as exc:
            raise PersistenceError(
                "Lecture des KPI pour la période impossible",
                operation="select",
                details=str(exc),
            ) from exc

        results: list[dict[str, object]] = []
        for row in rows:
            results.append(
                {
                    "code": row[0],
                    "label": row[1],
                    "value": row[2],
                    "unit": row[3],
                    "period_start": row[4],
                    "period_end": row[5],
                    "site": row[6],
                    "agent": row[7],
                    "channel": row[8],
                    "computed_at": row[9],
                }
            )
        logger.info(
            "%d KPI chargés pour la période %s → %s",
            len(results),
            period_start,
            period_end,
        )
        return results

    def delete_for_period(self, period_start: str, period_end: str) -> int:
        """Supprime tous les KPI d'une période (bornes inclusives).

        Utilisé pour rejouer le calcul sans dupliquer les lignes.

        :param period_start: Début ISO 8601 (date).
        :type period_start: str
        :param period_end: Fin ISO 8601 (date).
        :type period_end: str
        :return: Nombre de lignes supprimées.
        :rtype: int
        :raises PersistenceError: Si la suppression échoue.
        """
        conn = self.session_manager.connection
        try:
            cursor = conn.execute(
                f"DELETE FROM {self.TABLE_NAME} "  # noqa: S608
                "WHERE period_start = ? AND period_end = ?",
                (period_start, period_end),
            )
            conn.commit()
        except sqlite3.Error as exc:
            raise PersistenceError(
                "Suppression des KPI pour la période impossible",
                operation="delete",
                details=str(exc),
            ) from exc
        count: int = cursor.rowcount
        logger.info(
            "%d KPI supprimés pour la période %s → %s",
            count,
            period_start,
            period_end,
        )
        return count

    def delete_by_code(self, code: str) -> int:
        """Supprime les KPI par code.

        :param code: Code du KPI.
        :type code: str
        :return: Nombre de lignes supprimées.
        :rtype: int
        :raises PersistenceError: Si la suppression échoue.
        """
        conn = self.session_manager.connection
        try:
            cursor = conn.execute(
                f"DELETE FROM {self.TABLE_NAME} WHERE code = ?",  # noqa: S608
                (code,),
            )
            conn.commit()
        except sqlite3.Error as exc:
            raise PersistenceError(
                "Suppression des KPI impossible",
                operation="delete",
                details=str(exc),
            ) from exc
        count: int = cursor.rowcount
        logger.info("%d KPI supprimés pour le code '%s'", count, code)
        return count

    def __repr__(self) -> str:
        """Retourne une représentation technique du repository.

        :return: Représentation technique.
        :rtype: str
        """
        return f"KpiRepository(table={self.TABLE_NAME!r})"
