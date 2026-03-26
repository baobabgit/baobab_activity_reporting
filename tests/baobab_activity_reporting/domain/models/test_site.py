"""Tests unitaires pour Site."""

import pytest

from baobab_activity_reporting.domain.models.site import Site
from baobab_activity_reporting.exceptions.validation_error import (
    ValidationError,
)


class TestSite:
    """Tests pour la classe Site."""

    def test_creation_nominal(self) -> None:
        """Vérifie la création avec des données valides."""
        site = Site("S01", "Paris Nord")
        assert site.site_id == "S01"
        assert site.name == "Paris Nord"
        assert site.label is None

    def test_creation_with_label(self) -> None:
        """Vérifie la création avec un libellé."""
        site = Site("S01", "Paris Nord", label="SIE Paris Nord")
        assert site.label == "SIE Paris Nord"

    def test_strips_whitespace(self) -> None:
        """Vérifie que les espaces sont supprimés."""
        site = Site("  S01  ", "  Paris  ", label="  Label  ")
        assert site.site_id == "S01"
        assert site.name == "Paris"
        assert site.label == "Label"

    def test_empty_site_id_raises(self) -> None:
        """Vérifie l'exception pour un identifiant vide."""
        with pytest.raises(ValidationError, match="identifiant"):
            Site("", "Paris")

    def test_whitespace_site_id_raises(self) -> None:
        """Vérifie l'exception pour un identifiant ne contenant que des espaces."""
        with pytest.raises(ValidationError, match="identifiant"):
            Site("   ", "Paris")

    def test_empty_name_raises(self) -> None:
        """Vérifie l'exception pour un nom vide."""
        with pytest.raises(ValidationError, match="nom"):
            Site("S01", "")

    def test_display_label_with_label(self) -> None:
        """Vérifie le libellé d'affichage avec un label défini."""
        site = Site("S01", "Paris", label="SIE Paris")
        assert site.display_label == "SIE Paris"

    def test_display_label_without_label(self) -> None:
        """Vérifie le libellé d'affichage sans label (fallback sur name)."""
        site = Site("S01", "Paris")
        assert site.display_label == "Paris"

    def test_equality_by_id(self) -> None:
        """Vérifie l'égalité par identifiant."""
        s1 = Site("S01", "Paris")
        s2 = Site("S01", "Lyon")
        assert s1 == s2

    def test_inequality_by_id(self) -> None:
        """Vérifie l'inégalité par identifiant."""
        s1 = Site("S01", "Paris")
        s2 = Site("S02", "Paris")
        assert s1 != s2

    def test_equality_with_other_type(self) -> None:
        """Vérifie la comparaison avec un autre type."""
        site = Site("S01", "Paris")
        assert site != "not a site"

    def test_hash_by_id(self) -> None:
        """Vérifie que le hash est basé sur l'identifiant."""
        s1 = Site("S01", "Paris")
        s2 = Site("S01", "Lyon")
        assert hash(s1) == hash(s2)

    def test_hash_in_set(self) -> None:
        """Vérifie l'utilisation dans un set."""
        s1 = Site("S01", "Paris")
        s2 = Site("S01", "Lyon")
        assert len({s1, s2}) == 1

    def test_repr(self) -> None:
        """Vérifie __repr__."""
        site = Site("S01", "Paris")
        result = repr(site)
        assert "Site(" in result
        assert "site_id='S01'" in result

    def test_label_none_stays_none(self) -> None:
        """Vérifie que label=None reste None."""
        site = Site("S01", "Paris", label=None)
        assert site.label is None
