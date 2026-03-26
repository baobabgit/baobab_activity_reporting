"""Tests unitaires pour ReportDataRepository."""

import pytest

from baobab_activity_reporting.storage.repositories.report_data_repository import (
    ReportDataRepository,
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


class TestReportDataRepository:
    """Tests pour la classe ReportDataRepository."""

    def test_save_and_load(self, session: DatabaseSessionManager) -> None:
        """Vérifie le cycle save/load."""
        repo = ReportDataRepository(session)
        repo.save_section("telephony", "overview", '{"key": "val"}')
        results = repo.load_by_report_type("telephony")
        assert len(results) == 1
        assert results[0]["section_code"] == "overview"
        assert results[0]["content"] == '{"key": "val"}'

    def test_load_empty(self, session: DatabaseSessionManager) -> None:
        """Vérifie le chargement d'un type inexistant."""
        repo = ReportDataRepository(session)
        results = repo.load_by_report_type("missing")
        assert results == []

    def test_multiple_sections(self, session: DatabaseSessionManager) -> None:
        """Vérifie l'insertion de plusieurs sections."""
        repo = ReportDataRepository(session)
        repo.save_section("t", "s1", "c1")
        repo.save_section("t", "s2", "c2")
        results = repo.load_by_report_type("t")
        assert len(results) == 2

    def test_delete(self, session: DatabaseSessionManager) -> None:
        """Vérifie la suppression par type de rapport."""
        repo = ReportDataRepository(session)
        repo.save_section("t", "s", "c")
        deleted = repo.delete_by_report_type("t")
        assert deleted == 1
        assert repo.load_by_report_type("t") == []

    def test_delete_nonexistent(self, session: DatabaseSessionManager) -> None:
        """Vérifie la suppression d'un type inexistant."""
        repo = ReportDataRepository(session)
        deleted = repo.delete_by_report_type("nope")
        assert deleted == 0

    def test_isolation_between_types(self, session: DatabaseSessionManager) -> None:
        """Vérifie l'isolation entre types de rapport."""
        repo = ReportDataRepository(session)
        repo.save_section("type_a", "s1", "c1")
        repo.save_section("type_b", "s2", "c2")
        assert len(repo.load_by_report_type("type_a")) == 1
        assert len(repo.load_by_report_type("type_b")) == 1

    def test_repr(self, session: DatabaseSessionManager) -> None:
        """Vérifie __repr__."""
        repo = ReportDataRepository(session)
        assert "ReportDataRepository(" in repr(repo)

    def test_generated_at_populated(self, session: DatabaseSessionManager) -> None:
        """Vérifie que generated_at est automatiquement rempli."""
        repo = ReportDataRepository(session)
        repo.save_section("t", "s", "c")
        results = repo.load_by_report_type("t")
        assert results[0]["generated_at"] is not None
