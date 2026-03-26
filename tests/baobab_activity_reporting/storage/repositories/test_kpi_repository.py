"""Tests unitaires pour KpiRepository."""

import pytest

from baobab_activity_reporting.storage.repositories.kpi_repository import (
    KpiRepository,
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


class TestKpiRepository:
    """Tests pour la classe KpiRepository."""

    def test_save_and_load(self, session: DatabaseSessionManager) -> None:
        """Vérifie le cycle save/load."""
        repo = KpiRepository(session)
        repo.save_kpi("nb_appels", "Nombre d'appels", 42.0, "appels")
        results = repo.load_by_code("nb_appels")
        assert len(results) == 1
        assert results[0]["code"] == "nb_appels"
        assert results[0]["value"] == 42.0
        assert results[0]["unit"] == "appels"

    def test_save_with_period(self, session: DatabaseSessionManager) -> None:
        """Vérifie l'insertion avec période."""
        repo = KpiRepository(session)
        repo.save_kpi(
            "nb",
            "N",
            10.0,
            period_start="2026-01-01",
            period_end="2026-01-31",
        )
        results = repo.load_by_code("nb")
        assert results[0]["period_start"] == "2026-01-01"
        assert results[0]["period_end"] == "2026-01-31"

    def test_load_empty(self, session: DatabaseSessionManager) -> None:
        """Vérifie le chargement d'un code inexistant."""
        repo = KpiRepository(session)
        results = repo.load_by_code("missing")
        assert results == []

    def test_load_all(self, session: DatabaseSessionManager) -> None:
        """Vérifie le chargement de tous les KPI."""
        repo = KpiRepository(session)
        repo.save_kpi("a", "A", 1.0)
        repo.save_kpi("b", "B", 2.0)
        all_kpis = repo.load_all()
        assert len(all_kpis) == 2

    def test_load_all_empty(self, session: DatabaseSessionManager) -> None:
        """Vérifie load_all sur une base vide."""
        repo = KpiRepository(session)
        assert repo.load_all() == []

    def test_delete(self, session: DatabaseSessionManager) -> None:
        """Vérifie la suppression par code."""
        repo = KpiRepository(session)
        repo.save_kpi("del", "Delete", 0.0)
        deleted = repo.delete_by_code("del")
        assert deleted == 1
        assert repo.load_by_code("del") == []

    def test_delete_nonexistent(self, session: DatabaseSessionManager) -> None:
        """Vérifie la suppression d'un code inexistant."""
        repo = KpiRepository(session)
        deleted = repo.delete_by_code("nope")
        assert deleted == 0

    def test_multiple_kpi_same_code(self, session: DatabaseSessionManager) -> None:
        """Vérifie l'insertion de plusieurs KPI avec le même code."""
        repo = KpiRepository(session)
        repo.save_kpi("k", "K", 1.0)
        repo.save_kpi("k", "K", 2.0)
        results = repo.load_by_code("k")
        assert len(results) == 2

    def test_save_without_unit(self, session: DatabaseSessionManager) -> None:
        """Vérifie l'insertion sans unité."""
        repo = KpiRepository(session)
        repo.save_kpi("x", "X", 5.0)
        results = repo.load_by_code("x")
        assert results[0]["unit"] is None

    def test_repr(self, session: DatabaseSessionManager) -> None:
        """Vérifie __repr__."""
        repo = KpiRepository(session)
        assert "KpiRepository(" in repr(repo)
