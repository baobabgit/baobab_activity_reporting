"""Fixtures partagées entre tous les tests."""

from pathlib import Path

import pytest

FIXTURES_DIR = Path(__file__).parent / "fixtures"


@pytest.fixture()
def fixtures_dir() -> Path:
    """Retourne le chemin vers le répertoire de fixtures.

    :return: Chemin absolu du dossier ``tests/fixtures``.
    :rtype: Path
    """
    return FIXTURES_DIR
