"""Tests unitaires pour Kpi."""

import pytest

from baobab_activity_reporting.domain.models.kpi import Kpi
from baobab_activity_reporting.exceptions.validation_error import (
    ValidationError,
)


class TestKpi:
    """Tests pour la classe Kpi."""

    def test_creation_nominal(self) -> None:
        """Vérifie la création avec des données valides."""
        kpi = Kpi("nb_appels", "Nombre d'appels", 142.0)
        assert kpi.code == "nb_appels"
        assert kpi.label == "Nombre d'appels"
        assert kpi.value == 142.0
        assert kpi.unit is None

    def test_creation_with_unit(self) -> None:
        """Vérifie la création avec une unité."""
        kpi = Kpi("nb_appels", "Nombre d'appels", 142.0, unit="appels")
        assert kpi.unit == "appels"

    def test_strips_whitespace(self) -> None:
        """Vérifie que les espaces sont supprimés."""
        kpi = Kpi("  code  ", "  label  ", 1.0, unit="  u  ")
        assert kpi.code == "code"
        assert kpi.label == "label"
        assert kpi.unit == "u"

    def test_empty_code_raises(self) -> None:
        """Vérifie l'exception pour un code vide."""
        with pytest.raises(ValidationError, match="code"):
            Kpi("", "Label", 0.0)

    def test_whitespace_code_raises(self) -> None:
        """Vérifie l'exception pour un code ne contenant que des espaces."""
        with pytest.raises(ValidationError, match="code"):
            Kpi("   ", "Label", 0.0)

    def test_empty_label_raises(self) -> None:
        """Vérifie l'exception pour un libellé vide."""
        with pytest.raises(ValidationError, match="libellé"):
            Kpi("code", "", 0.0)

    def test_formatted_value_with_unit(self) -> None:
        """Vérifie la valeur formatée avec unité."""
        kpi = Kpi("k", "l", 42.5, unit="%")
        assert kpi.formatted_value == "42.5 %"

    def test_formatted_value_without_unit(self) -> None:
        """Vérifie la valeur formatée sans unité."""
        kpi = Kpi("k", "l", 42.0)
        assert kpi.formatted_value == "42.0"

    def test_zero_value(self) -> None:
        """Vérifie un KPI avec une valeur à zéro."""
        kpi = Kpi("k", "l", 0.0)
        assert kpi.value == 0.0

    def test_negative_value(self) -> None:
        """Vérifie un KPI avec une valeur négative."""
        kpi = Kpi("k", "l", -5.3)
        assert kpi.value == -5.3

    def test_equality_by_code(self) -> None:
        """Vérifie l'égalité par code."""
        k1 = Kpi("nb_appels", "Label 1", 10.0)
        k2 = Kpi("nb_appels", "Label 2", 20.0)
        assert k1 == k2

    def test_inequality_by_code(self) -> None:
        """Vérifie l'inégalité par code."""
        k1 = Kpi("nb_appels", "L", 10.0)
        k2 = Kpi("nb_tickets", "L", 10.0)
        assert k1 != k2

    def test_equality_with_other_type(self) -> None:
        """Vérifie la comparaison avec un autre type."""
        kpi = Kpi("k", "l", 0.0)
        assert kpi != "not a kpi"

    def test_hash_by_code(self) -> None:
        """Vérifie que le hash est basé sur le code."""
        k1 = Kpi("nb_appels", "L1", 10.0)
        k2 = Kpi("nb_appels", "L2", 20.0)
        assert hash(k1) == hash(k2)

    def test_hash_in_set(self) -> None:
        """Vérifie l'utilisation dans un set."""
        k1 = Kpi("nb_appels", "L1", 10.0)
        k2 = Kpi("nb_appels", "L2", 20.0)
        assert len({k1, k2}) == 1

    def test_repr(self) -> None:
        """Vérifie __repr__."""
        kpi = Kpi("k", "l", 1.0)
        result = repr(kpi)
        assert "Kpi(" in result
        assert "code='k'" in result

    def test_unit_none_stays_none(self) -> None:
        """Vérifie que unit=None reste None."""
        kpi = Kpi("k", "l", 1.0, unit=None)
        assert kpi.unit is None
