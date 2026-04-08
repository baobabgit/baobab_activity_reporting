"""Tests pour WritingStyle."""

from baobab_activity_reporting.reporting.editorial.writing_style import WritingStyle


class TestWritingStyle:
    """Tests pour la classe WritingStyle."""

    def test_default(self) -> None:
        """Style par défaut."""
        w = WritingStyle.default()
        assert w.tone == "professionnel"
