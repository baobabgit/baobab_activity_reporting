"""Tests unitaires pour Agent."""

import pytest

from baobab_activity_reporting.domain.models.agent import Agent
from baobab_activity_reporting.exceptions.validation_error import (
    ValidationError,
)


class TestAgent:
    """Tests pour la classe Agent."""

    def test_creation_nominal(self) -> None:
        """Vérifie la création avec des données valides."""
        agent = Agent("A001", "Dupont", "Marie")
        assert agent.agent_id == "A001"
        assert agent.last_name == "Dupont"
        assert agent.first_name == "Marie"
        assert agent.site_name is None

    def test_creation_with_site(self) -> None:
        """Vérifie la création avec un site."""
        agent = Agent("A001", "Dupont", "Marie", site_name="Paris")
        assert agent.site_name == "Paris"

    def test_strips_whitespace(self) -> None:
        """Vérifie que les espaces sont supprimés."""
        agent = Agent("  A001  ", "  Dupont  ", "  Marie  ", "  Paris  ")
        assert agent.agent_id == "A001"
        assert agent.last_name == "Dupont"
        assert agent.first_name == "Marie"
        assert agent.site_name == "Paris"

    def test_empty_agent_id_raises(self) -> None:
        """Vérifie l'exception pour un identifiant vide."""
        with pytest.raises(ValidationError, match="identifiant"):
            Agent("", "Dupont", "Marie")

    def test_whitespace_agent_id_raises(self) -> None:
        """Vérifie l'exception pour un identifiant ne contenant que des espaces."""
        with pytest.raises(ValidationError, match="identifiant"):
            Agent("   ", "Dupont", "Marie")

    def test_empty_last_name_raises(self) -> None:
        """Vérifie l'exception pour un nom vide."""
        with pytest.raises(ValidationError, match="nom"):
            Agent("A001", "", "Marie")

    def test_empty_first_name_raises(self) -> None:
        """Vérifie l'exception pour un prénom vide."""
        with pytest.raises(ValidationError, match="prénom"):
            Agent("A001", "Dupont", "")

    def test_full_name(self) -> None:
        """Vérifie le nom complet."""
        agent = Agent("A001", "Dupont", "Marie")
        assert agent.full_name == "Marie Dupont"

    def test_equality_by_id(self) -> None:
        """Vérifie l'égalité par identifiant."""
        a1 = Agent("A001", "Dupont", "Marie")
        a2 = Agent("A001", "Martin", "Jean")
        assert a1 == a2

    def test_inequality_by_id(self) -> None:
        """Vérifie l'inégalité par identifiant."""
        a1 = Agent("A001", "Dupont", "Marie")
        a2 = Agent("A002", "Dupont", "Marie")
        assert a1 != a2

    def test_equality_with_other_type(self) -> None:
        """Vérifie la comparaison avec un autre type."""
        agent = Agent("A001", "Dupont", "Marie")
        assert agent != "not an agent"

    def test_hash_by_id(self) -> None:
        """Vérifie que le hash est basé sur l'identifiant."""
        a1 = Agent("A001", "Dupont", "Marie")
        a2 = Agent("A001", "Martin", "Jean")
        assert hash(a1) == hash(a2)

    def test_hash_in_set(self) -> None:
        """Vérifie l'utilisation dans un set."""
        a1 = Agent("A001", "Dupont", "Marie")
        a2 = Agent("A001", "Martin", "Jean")
        assert len({a1, a2}) == 1

    def test_repr(self) -> None:
        """Vérifie __repr__."""
        agent = Agent("A001", "Dupont", "Marie")
        result = repr(agent)
        assert "Agent(" in result
        assert "agent_id='A001'" in result

    def test_site_name_none_stays_none(self) -> None:
        """Vérifie que site_name=None reste None."""
        agent = Agent("A001", "Dupont", "Marie", site_name=None)
        assert agent.site_name is None
