"""Tests unitaires pour PackageMetadata."""

from unittest.mock import patch

import pytest

from baobab_activity_reporting.core.package_metadata import PackageMetadata
from baobab_activity_reporting.exceptions.configuration_exception import (
    ConfigurationException,
)


class TestPackageMetadata:
    """Tests pour la classe PackageMetadata."""

    def test_name_is_set(self) -> None:
        """Vérifie que le nom du package est correct."""
        meta = PackageMetadata()
        assert meta.name == "baobab-activity-reporting"

    def test_version_is_string(self) -> None:
        """Vérifie que la version est une chaîne."""
        meta = PackageMetadata()
        assert isinstance(meta.package_version, str)

    def test_version_follows_semver(self) -> None:
        """Vérifie que la version suit le format sémantique."""
        meta = PackageMetadata()
        parts = meta.package_version.split(".")
        assert len(parts) == 3
        for part in parts:
            assert part.isdigit()

    def test_summary(self) -> None:
        """Vérifie le format du résumé."""
        meta = PackageMetadata()
        summary = meta.summary()
        assert summary.startswith("baobab-activity-reporting v")

    def test_repr(self) -> None:
        """Vérifie __repr__."""
        meta = PackageMetadata()
        result = repr(meta)
        assert "PackageMetadata(" in result
        assert "name='baobab-activity-reporting'" in result
        assert "package_version=" in result

    def test_raises_when_not_installed(self) -> None:
        """Vérifie l'exception si le package n'est pas installé."""
        from importlib.metadata import PackageNotFoundError

        with patch(
            "baobab_activity_reporting.core.package_metadata.version",
            side_effect=PackageNotFoundError("not found"),
        ):
            with pytest.raises(ConfigurationException, match="non installé"):
                PackageMetadata()

    def test_version_matches_pyproject(self) -> None:
        """Vérifie que la version correspond à celle du pyproject."""
        meta = PackageMetadata()
        assert meta.package_version == "0.7.0"
