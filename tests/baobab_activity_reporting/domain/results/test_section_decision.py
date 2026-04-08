"""Tests unitaires pour SectionDecision et SectionStatus."""

from baobab_activity_reporting.domain.results.section_decision import (
    SectionDecision,
    SectionStatus,
)


class TestSectionStatus:
    """Tests pour l'énumération SectionStatus."""

    def test_included_value(self) -> None:
        """Vérifie la valeur de INCLUDED."""
        assert SectionStatus.INCLUDED.value == "included"

    def test_excluded_value(self) -> None:
        """Vérifie la valeur de EXCLUDED."""
        assert SectionStatus.EXCLUDED.value == "excluded"

    def test_degraded_value(self) -> None:
        """Vérifie la valeur de DEGRADED."""
        assert SectionStatus.DEGRADED.value == "degraded"


class TestSectionDecision:
    """Tests pour la classe SectionDecision."""

    def test_creation_included(self) -> None:
        """Vérifie la création d'une décision d'inclusion."""
        decision = SectionDecision("tel_overview", SectionStatus.INCLUDED)
        assert decision.section_code == "tel_overview"
        assert decision.status == SectionStatus.INCLUDED
        assert decision.reason is None

    def test_creation_excluded_with_reason(self) -> None:
        """Vérifie la création d'une exclusion avec raison."""
        decision = SectionDecision(
            "tel_overview",
            SectionStatus.EXCLUDED,
            reason="Données insuffisantes",
        )
        assert decision.status == SectionStatus.EXCLUDED
        assert decision.reason == "Données insuffisantes"

    def test_creation_degraded(self) -> None:
        """Vérifie la création d'une décision dégradée."""
        decision = SectionDecision(
            "agent_detail",
            SectionStatus.DEGRADED,
            reason="Données partielles",
        )
        assert decision.status == SectionStatus.DEGRADED

    def test_is_included_when_included(self) -> None:
        """Vérifie is_included pour INCLUDED."""
        decision = SectionDecision("s", SectionStatus.INCLUDED)
        assert decision.is_included is True

    def test_is_included_when_degraded(self) -> None:
        """Vérifie is_included pour DEGRADED."""
        decision = SectionDecision("s", SectionStatus.DEGRADED)
        assert decision.is_included is True

    def test_is_included_when_excluded(self) -> None:
        """Vérifie is_included pour EXCLUDED."""
        decision = SectionDecision("s", SectionStatus.EXCLUDED)
        assert decision.is_included is False

    def test_repr(self) -> None:
        """Vérifie __repr__."""
        decision = SectionDecision("s", SectionStatus.INCLUDED)
        text = repr(decision)
        assert "SectionDecision(" in text
        assert "section_code='s'" in text
        assert "detail=None" in text
