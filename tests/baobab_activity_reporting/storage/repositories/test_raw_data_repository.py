"""Tests unitaires pour RawDataRepository."""

import pandas as pd
import pytest

from baobab_activity_reporting.storage.repositories.raw_data_repository import (
    RawDataRepository,
)
from baobab_activity_reporting.storage.sqlite.database_session_manager import (
    DatabaseSessionManager,
)


@pytest.fixture()
def session() -> DatabaseSessionManager:
    """Fournit un session manager en mémoire.

    :return: Session manager.
    :rtype: DatabaseSessionManager
    """
    mgr = DatabaseSessionManager(":memory:")
    yield mgr  # type: ignore[misc]
    mgr.close()


class TestRawDataRepository:
    """Tests pour la classe RawDataRepository."""

    def test_save_and_load(self, session: DatabaseSessionManager) -> None:
        """Vérifie le cycle save/load."""
        repo = RawDataRepository(session)
        df = pd.DataFrame({"col1": [1, 2], "col2": ["a", "b"]})
        count = repo.save(df, "src1")
        assert count == 2
        loaded = repo.load("src1")
        assert len(loaded) == 2
        assert "col1" in loaded.columns

    def test_load_empty(self, session: DatabaseSessionManager) -> None:
        """Vérifie le chargement d'une source inexistante."""
        repo = RawDataRepository(session)
        loaded = repo.load("missing")
        assert len(loaded) == 0

    def test_count(self, session: DatabaseSessionManager) -> None:
        """Vérifie le comptage."""
        repo = RawDataRepository(session)
        df = pd.DataFrame({"a": [1, 2, 3]})
        repo.save(df, "src")
        assert repo.count("src") == 3
        assert repo.count("other") == 0

    def test_delete(self, session: DatabaseSessionManager) -> None:
        """Vérifie la suppression."""
        repo = RawDataRepository(session)
        df = pd.DataFrame({"a": [1, 2]})
        repo.save(df, "src")
        deleted = repo.delete("src")
        assert deleted == 2
        assert repo.count("src") == 0

    def test_delete_nonexistent(self, session: DatabaseSessionManager) -> None:
        """Vérifie la suppression d'une source inexistante."""
        repo = RawDataRepository(session)
        deleted = repo.delete("nope")
        assert deleted == 0

    def test_multiple_sources(self, session: DatabaseSessionManager) -> None:
        """Vérifie l'isolation entre sources."""
        repo = RawDataRepository(session)
        repo.save(pd.DataFrame({"x": [1]}), "s1")
        repo.save(pd.DataFrame({"x": [2, 3]}), "s2")
        assert repo.count("s1") == 1
        assert repo.count("s2") == 2

    def test_save_empty_dataframe(self, session: DatabaseSessionManager) -> None:
        """Vérifie l'insertion d'un DataFrame vide."""
        repo = RawDataRepository(session)
        count = repo.save(pd.DataFrame(), "empty")
        assert count == 0

    def test_repr(self, session: DatabaseSessionManager) -> None:
        """Vérifie __repr__."""
        repo = RawDataRepository(session)
        assert "RawDataRepository(" in repr(repo)
