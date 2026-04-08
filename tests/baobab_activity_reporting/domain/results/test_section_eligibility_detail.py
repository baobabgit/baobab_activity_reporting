"""Tests pour SectionEligibilityDetail."""

from baobab_activity_reporting.domain.results.section_eligibility_detail import (
    SectionEligibilityDetail,
)


class TestSectionEligibilityDetail:
    """Couverture du détail d'éligibilité."""

    def test_frozen_slots(self) -> None:
        """Dataclass immuable avec emplacements."""
        d = SectionEligibilityDetail(
            codes=frozenset({"a"}),
            notes=("n",),
        )
        assert d.codes == frozenset({"a"})
        assert d.notes == ("n",)
