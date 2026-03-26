"""Tests unitaires pour DataAvailability."""

from baobab_activity_reporting.domain.results.data_availability import (
    DataAvailability,
)


class TestDataAvailability:
    """Tests pour la classe DataAvailability."""

    def test_creation_available(self) -> None:
        """Vérifie la création avec données disponibles."""
        avail = DataAvailability("appels", True, 120)
        assert avail.source_name == "appels"
        assert avail.available is True
        assert avail.row_count == 120
        assert avail.reason is None

    def test_creation_unavailable(self) -> None:
        """Vérifie la création avec données indisponibles."""
        avail = DataAvailability("tickets", False, 0, reason="Fichier absent")
        assert avail.available is False
        assert avail.reason == "Fichier absent"

    def test_default_row_count(self) -> None:
        """Vérifie la valeur par défaut de row_count."""
        avail = DataAvailability("s", True)
        assert avail.row_count == 0

    def test_is_sufficient_true(self) -> None:
        """Vérifie is_sufficient quand les données sont suffisantes."""
        avail = DataAvailability("s", True, 100)
        assert avail.is_sufficient(min_rows=10) is True

    def test_is_sufficient_exact_threshold(self) -> None:
        """Vérifie is_sufficient au seuil exact."""
        avail = DataAvailability("s", True, 10)
        assert avail.is_sufficient(min_rows=10) is True

    def test_is_sufficient_below_threshold(self) -> None:
        """Vérifie is_sufficient sous le seuil."""
        avail = DataAvailability("s", True, 5)
        assert avail.is_sufficient(min_rows=10) is False

    def test_is_sufficient_false_when_unavailable(self) -> None:
        """Vérifie is_sufficient quand indisponible."""
        avail = DataAvailability("s", False, 100)
        assert avail.is_sufficient(min_rows=1) is False

    def test_is_sufficient_default_min_rows(self) -> None:
        """Vérifie is_sufficient avec le seuil par défaut (1)."""
        avail = DataAvailability("s", True, 1)
        assert avail.is_sufficient() is True

    def test_is_sufficient_zero_rows_default(self) -> None:
        """Vérifie is_sufficient avec 0 lignes et seuil par défaut."""
        avail = DataAvailability("s", True, 0)
        assert avail.is_sufficient() is False

    def test_repr(self) -> None:
        """Vérifie __repr__."""
        avail = DataAvailability("s", True, 50)
        text = repr(avail)
        assert "DataAvailability(" in text
        assert "source_name='s'" in text
        assert "available=True" in text
        assert "row_count=50" in text
