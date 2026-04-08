"""Tests pour EditorialSectionDefinition."""

import pytest

from baobab_activity_reporting.exceptions.report_generation_error import (
    ReportGenerationError,
)
from baobab_activity_reporting.reporting.editorial.display_rules import DisplayRules
from baobab_activity_reporting.reporting.editorial.editorial_section_definition import (
    EditorialSectionDefinition,
)
from baobab_activity_reporting.reporting.editorial.section_visibility_rule import (
    SectionVisibilityRule,
)
from baobab_activity_reporting.reporting.editorial.table_policy import TablePolicy
from baobab_activity_reporting.reporting.editorial.writing_style import WritingStyle


class TestEditorialSectionDefinition:
    """Tests pour la classe EditorialSectionDefinition."""

    def test_legacy_triplet(self) -> None:
        """Vue legacy cohérente avec les préfixes."""
        ed = EditorialSectionDefinition(
            section_code="x",
            section_title="T",
            section_objective="Obj",
            required_data=frozenset(),
            optional_data=frozenset(),
            display_rules=DisplayRules.default(),
            writing_style=WritingStyle.default(),
            visibility_rule=SectionVisibilityRule.from_prefixes(frozenset({"a."})),
            table_policy=TablePolicy.default(),
        )
        assert ed.legacy_triplet() == ("x", "T", frozenset({"a."}))

    def test_empty_section_code_raises(self) -> None:
        """Code vide interdit."""
        with pytest.raises(ReportGenerationError):
            EditorialSectionDefinition(
                section_code="   ",
                section_title="T",
                section_objective="",
                required_data=frozenset(),
                optional_data=frozenset(),
                display_rules=DisplayRules.default(),
                writing_style=WritingStyle.default(),
                visibility_rule=SectionVisibilityRule.from_prefixes(frozenset()),
                table_policy=TablePolicy.default(),
            )

    def test_empty_section_title_raises(self) -> None:
        """Titre vide interdit."""
        with pytest.raises(ReportGenerationError):
            EditorialSectionDefinition(
                section_code="c",
                section_title="  ",
                section_objective="",
                required_data=frozenset(),
                optional_data=frozenset(),
                display_rules=DisplayRules.default(),
                writing_style=WritingStyle.default(),
                visibility_rule=SectionVisibilityRule.from_prefixes(frozenset()),
                table_policy=TablePolicy.default(),
            )
