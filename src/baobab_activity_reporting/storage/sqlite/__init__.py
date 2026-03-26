"""Sous-package de la couche SQLite.

Contient le gestionnaire de connexion SQLite.
"""

from baobab_activity_reporting.storage.sqlite.database_session_manager import (
    DatabaseSessionManager,
)

__all__: list[str] = [
    "DatabaseSessionManager",
]
