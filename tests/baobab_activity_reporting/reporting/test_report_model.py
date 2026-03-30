"""Tests unitaires pour ReportModel."""

from baobab_activity_reporting.reporting.report_model import ReportModel


class TestReportModel:
    """Tests pour la classe ReportModel."""

    def test_section_codes(self) -> None:
        """Vérifie l'extraction des codes."""
        m = ReportModel(
            "t",
            "T",
            "2026-01-01",
            "2026-01-31",
            [],
            [{"section_code": "a"}, {"section_code": "b"}],
        )
        assert m.section_codes == ["a", "b"]

    def test_to_document_tree(self) -> None:
        """Vérifie l'export arborescent."""
        m = ReportModel(
            "t",
            "T",
            "2026-01-01",
            "2026-01-31",
            ["intro"],
            [{"section_code": "s", "tables": []}],
        )
        tree = m.to_document_tree()
        assert tree["title"] == "T"
        assert tree["preamble_narratives"] == ["intro"]
