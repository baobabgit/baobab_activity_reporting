"""Tests unitaires pour DocxWriter."""

from pathlib import Path

import pytest
from docx import Document as DocxRead

from baobab_activity_reporting.exceptions.writer_error import WriterError
from baobab_activity_reporting.reporting.report_model import ReportModel
from baobab_activity_reporting.reporting.writers.docx_writer import DocxWriter


class TestDocxWriter:
    """Tests pour la classe DocxWriter."""

    def test_write_minimal_report(self, tmp_path: Path) -> None:
        """Génère un DOCX lisible avec titre et préambule."""
        model = ReportModel(
            "t",
            "Rapport test",
            "2026-01-01",
            "2026-01-31",
            ["Introduction du rapport."],
            [],
        )
        out = tmp_path / "out.docx"
        DocxWriter().write(model, out)
        assert out.is_file()
        doc = DocxRead(str(out))
        texts = [p.text for p in doc.paragraphs if p.text.strip()]
        assert any("Rapport test" in t for t in texts)
        assert any("Introduction du rapport." in t for t in texts)

    def test_write_with_section_table_and_insights(self, tmp_path: Path) -> None:
        """Section avec tableau et points saillants."""
        section = {
            "section_code": "s1",
            "title": "Synthèse",
            "narrative_blocks": ["Texte de section."],
            "tables": [
                {
                    "caption": "Indicateurs",
                    "headers": ["Code", "Valeur"],
                    "rows": [["a", "1"]],
                }
            ],
            "insights": ["Premier insight."],
        }
        model = ReportModel("t", "T", "2026-01-01", "2026-01-31", [], [section])
        out = tmp_path / "full.docx"
        DocxWriter().write(model, out)
        doc = DocxRead(str(out))
        full_text = "\n".join(p.text for p in doc.paragraphs)
        assert "Synthèse" in full_text
        assert "Indicateurs" in full_text
        assert "Premier insight." in full_text

    def test_write_raises_writer_error_on_blocked_parent(self, tmp_path: Path) -> None:
        """Un chemin invalide lève WriterError."""
        blocker = tmp_path / "not_a_directory"
        blocker.write_text("x", encoding="utf-8")
        model = ReportModel("t", "T", "a", "b", [], [])
        with pytest.raises(WriterError, match="DOCX"):
            DocxWriter().write(model, blocker / "nested.docx")
