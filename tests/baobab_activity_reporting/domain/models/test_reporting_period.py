"""Tests unitaires pour ReportingPeriod."""

from datetime import date

import pytest

from baobab_activity_reporting.domain.models.reporting_period import (
    ReportingPeriod,
)
from baobab_activity_reporting.exceptions.validation_error import (
    ValidationError,
)


class TestReportingPeriod:
    """Tests pour la classe ReportingPeriod."""

    def test_creation_nominal(self) -> None:
        """Vérifie la création avec des dates valides."""
        period = ReportingPeriod(date(2026, 1, 1), date(2026, 1, 31))
        assert period.start_date == date(2026, 1, 1)
        assert period.end_date == date(2026, 1, 31)

    def test_creation_same_dates(self) -> None:
        """Vérifie la création quand début et fin sont identiques."""
        period = ReportingPeriod(date(2026, 3, 1), date(2026, 3, 1))
        assert period.duration_days == 1

    def test_creation_invalid_dates_raises(self) -> None:
        """Vérifie l'exception si fin < début."""
        with pytest.raises(ValidationError, match="antérieure"):
            ReportingPeriod(date(2026, 2, 1), date(2026, 1, 1))

    def test_duration_days(self) -> None:
        """Vérifie le calcul du nombre de jours."""
        period = ReportingPeriod(date(2026, 1, 1), date(2026, 1, 31))
        assert period.duration_days == 31

    def test_duration_days_one_day(self) -> None:
        """Vérifie le nombre de jours pour une seule journée."""
        period = ReportingPeriod(date(2026, 6, 15), date(2026, 6, 15))
        assert period.duration_days == 1

    def test_contains_date_inside(self) -> None:
        """Vérifie qu'une date incluse est détectée."""
        period = ReportingPeriod(date(2026, 1, 1), date(2026, 1, 31))
        assert period.contains(date(2026, 1, 15)) is True

    def test_contains_date_start(self) -> None:
        """Vérifie que la date de début est incluse."""
        period = ReportingPeriod(date(2026, 1, 1), date(2026, 1, 31))
        assert period.contains(date(2026, 1, 1)) is True

    def test_contains_date_end(self) -> None:
        """Vérifie que la date de fin est incluse."""
        period = ReportingPeriod(date(2026, 1, 1), date(2026, 1, 31))
        assert period.contains(date(2026, 1, 31)) is True

    def test_contains_date_outside(self) -> None:
        """Vérifie qu'une date extérieure n'est pas incluse."""
        period = ReportingPeriod(date(2026, 1, 1), date(2026, 1, 31))
        assert period.contains(date(2026, 2, 1)) is False

    def test_equality(self) -> None:
        """Vérifie l'égalité entre deux périodes identiques."""
        p1 = ReportingPeriod(date(2026, 1, 1), date(2026, 1, 31))
        p2 = ReportingPeriod(date(2026, 1, 1), date(2026, 1, 31))
        assert p1 == p2

    def test_inequality(self) -> None:
        """Vérifie l'inégalité entre deux périodes différentes."""
        p1 = ReportingPeriod(date(2026, 1, 1), date(2026, 1, 31))
        p2 = ReportingPeriod(date(2026, 2, 1), date(2026, 2, 28))
        assert p1 != p2

    def test_equality_with_other_type(self) -> None:
        """Vérifie que la comparaison avec un autre type retourne NotImplemented."""
        period = ReportingPeriod(date(2026, 1, 1), date(2026, 1, 31))
        assert period != "not a period"

    def test_repr(self) -> None:
        """Vérifie __repr__."""
        period = ReportingPeriod(date(2026, 1, 1), date(2026, 1, 31))
        result = repr(period)
        assert "ReportingPeriod(" in result
        assert "start_date=" in result
        assert "end_date=" in result
