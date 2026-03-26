"""Tests unitaires pour PreparedDataRepository."""

import pandas as pd
import pytest

from baobab_activity_reporting.storage.repositories.prepared_data_repository import (
    PreparedDataRepository,
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


class TestPreparedDataRepository:
    """Tests pour la classe PreparedDataRepository."""

    def test_save_and_load(self, session: DatabaseSessionManager) -> None:
        """Vérifie le cycle save/load."""
        repo = PreparedDataRepository(session)
        df = pd.DataFrame({"col": [10, 20]})
        count = repo.save(df, "prep_src")
        assert count == 2
        loaded = repo.load("prep_src")
        assert len(loaded) == 2

    def test_load_empty(self, session: DatabaseSessionManager) -> None:
        """Vérifie le chargement d'une source inexistante."""
        repo = PreparedDataRepository(session)
        loaded = repo.load("missing")
        assert len(loaded) == 0

    def test_count(self, session: DatabaseSessionManager) -> None:
        """Vérifie le comptage."""
        repo = PreparedDataRepository(session)
        df = pd.DataFrame({"a": [1, 2, 3]})
        repo.save(df, "src")
        assert repo.count("src") == 3

    def test_delete(self, session: DatabaseSessionManager) -> None:
        """Vérifie la suppression."""
        repo = PreparedDataRepository(session)
        df = pd.DataFrame({"a": [1]})
        repo.save(df, "src")
        deleted = repo.delete("src")
        assert deleted == 1

    def test_delete_nonexistent(self, session: DatabaseSessionManager) -> None:
        """Vérifie la suppression d'une source inexistante."""
        repo = PreparedDataRepository(session)
        deleted = repo.delete("nope")
        assert deleted == 0

    def test_save_empty_dataframe(self, session: DatabaseSessionManager) -> None:
        """Vérifie l'insertion d'un DataFrame vide."""
        repo = PreparedDataRepository(session)
        count = repo.save(pd.DataFrame(), "empty")
        assert count == 0

    def test_repr(self, session: DatabaseSessionManager) -> None:
        """Vérifie __repr__."""
        repo = PreparedDataRepository(session)
        assert "PreparedDataRepository(" in repr(repo)
