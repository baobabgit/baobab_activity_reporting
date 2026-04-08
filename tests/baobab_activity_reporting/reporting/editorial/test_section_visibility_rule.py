"""Tests pour SectionVisibilityRule."""

from baobab_activity_reporting.reporting.editorial.section_visibility_rule import (
    SectionVisibilityRule,
)


class TestSectionVisibilityRule:
    """Tests pour la classe SectionVisibilityRule."""

    def test_from_prefixes(self) -> None:
        """Fabrique avec préfixes et obligation."""
        r = SectionVisibilityRule.from_prefixes(
            frozenset({"x."}),
            mandatory_in_report=True,
        )
        assert r.kpi_prefixes == frozenset({"x."})
        assert r.mandatory_in_report is True
