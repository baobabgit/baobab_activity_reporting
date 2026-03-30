"""Tests d'intégration export DOCX + Markdown depuis un ReportModel."""

from pathlib import Path

from docx import Document as DocxRead

from baobab_activity_reporting.reporting.report_model import ReportModel
from baobab_activity_reporting.reporting.writers.docx_writer import DocxWriter
from baobab_activity_reporting.reporting.writers.markdown_writer import (
    MarkdownWriter,
)


class TestWritersIntegration:
    """Export combiné pour un même modèle."""

    def test_same_model_two_formats(self, tmp_path: Path) -> None:
        """Un modèle simple produit deux fichiers exploitables."""
        model = ReportModel(
            "int",
            "Export double",
            "2026-03-01",
            "2026-03-31",
            ["Contexte partagé."],
            [
                {
                    "section_code": "kpi",
                    "title": "Chiffres",
                    "narrative_blocks": ["Détail."],
                    "tables": [
                        {
                            "caption": "Vue",
                            "headers": ["K", "V"],
                            "rows": [["x", "1"]],
                        }
                    ],
                    "insights": ["Lecture rapide."],
                }
            ],
        )
        docx_path = tmp_path / "rep.docx"
        md_path = tmp_path / "rep.md"
        DocxWriter().write(model, docx_path)
        MarkdownWriter().write(model, md_path)
        assert docx_path.stat().st_size > 0
        md_body = md_path.read_text(encoding="utf-8")
        assert "Export double" in md_body
        docx = DocxRead(str(docx_path))
        joined = " ".join(p.text for p in docx.paragraphs)
        assert "Chiffres" in joined
