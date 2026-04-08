"""Tests pour SectionAttentionAssessment."""

from baobab_activity_reporting.domain.results.section_attention_assessment import (
    SectionAttentionAssessment,
)


class TestSectionAttentionAssessment:
    """Couverture de l'évaluation vigilance."""

    def test_fields(self) -> None:
        """Champs accessibles."""
        a = SectionAttentionAssessment(
            has_attention_points=True,
            signal_codes=frozenset({"x"}),
            notes=("y",),
        )
        assert a.has_attention_points is True
        assert "x" in a.signal_codes
