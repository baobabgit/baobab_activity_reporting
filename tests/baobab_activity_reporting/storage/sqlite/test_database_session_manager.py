"""Tests unitaires pour DatabaseSessionManager."""

from pathlib import Path

import pytest

from baobab_activity_reporting.exceptions.persistence_error import (
    PersistenceError,
)
from baobab_activity_reporting.storage.sqlite.database_session_manager import (
    DatabaseSessionManager,
)


class TestDatabaseSessionManager:
    """Tests pour la classe DatabaseSessionManager."""

    def test_memory_connection(self) -> None:
        """Vérifie la connexion en mémoire."""
        manager = DatabaseSessionManager(":memory:")
        assert manager.is_open is True
        manager.close()

    def test_file_connection(self, tmp_path: Path) -> None:
        """Vérifie la connexion sur fichier."""
        db = str(tmp_path / "test.db")
        manager = DatabaseSessionManager(db)
        assert manager.is_open is True
        assert manager.file_exists() is True
        manager.close()

    def test_schema_created(self) -> None:
        """Vérifie que les tables sont créées."""
        manager = DatabaseSessionManager(":memory:")
        conn = manager.connection
        cursor = conn.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = {row[0] for row in cursor.fetchall()}
        assert "raw_data" in tables
        assert "prepared_data" in tables
        assert "kpi_data" in tables
        assert "report_data" in tables
        manager.close()

    def test_connection_property(self) -> None:
        """Vérifie l'accès à la connexion."""
        manager = DatabaseSessionManager(":memory:")
        conn = manager.connection
        assert conn is not None
        manager.close()

    def test_connection_after_close_raises(self) -> None:
        """Vérifie l'exception après fermeture."""
        manager = DatabaseSessionManager(":memory:")
        manager.close()
        with pytest.raises(PersistenceError, match="fermée"):
            _ = manager.connection

    def test_close_idempotent(self) -> None:
        """Vérifie que close est idempotent."""
        manager = DatabaseSessionManager(":memory:")
        manager.close()
        assert manager.is_open is False
        manager.close()
        assert manager.is_open is False

    def test_is_open_after_close(self) -> None:
        """Vérifie is_open après fermeture."""
        manager = DatabaseSessionManager(":memory:")
        assert manager.is_open is True
        manager.close()
        assert manager.is_open is False

    def test_file_exists_memory(self) -> None:
        """Vérifie file_exists pour une base en mémoire."""
        manager = DatabaseSessionManager(":memory:")
        assert manager.file_exists() is False
        manager.close()

    def test_repr(self) -> None:
        """Vérifie __repr__."""
        manager = DatabaseSessionManager(":memory:")
        result = repr(manager)
        assert "DatabaseSessionManager(" in result
        assert ":memory:" in result
        manager.close()

    def test_db_path_stored(self) -> None:
        """Vérifie que le chemin est stocké."""
        manager = DatabaseSessionManager(":memory:")
        assert manager.db_path == ":memory:"
        manager.close()
