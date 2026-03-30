"""Tests unitaires pour MarkdownWriter."""

from pathlib import Path

import pytest

from baobab_activity_reporting.exceptions.writer_error import WriterError
from baobab_activity_reporting.reporting.report_model import ReportModel
from baobab_activity_reporting.reporting.writers.markdown_writer import (
    MarkdownWriter,
)


class TestMarkdownWriter:
    """Tests pour la classe MarkdownWriter."""

    def test_write_contains_structure(self, tmp_path: Path) -> None:
        """Le Markdown contient titres, tableau et liste."""
        section = {
            "section_code": "s",
            "title": "Une section",
            "narrative_blocks": ["Paragraphe."],
            "tables": [
                {
                    "caption": "Tab",
                    "headers": ["A", "B"],
                    "rows": [[1, 2], [3, 4]],
                }
            ],
            "insights": ["Note"],
        }
        model = ReportModel(
            "mt",
            "Titre MD",
            "2026-02-01",
            "2026-02-28",
            ["Préambule"],
            [section],
        )
        out = tmp_path / "r.md"
        MarkdownWriter().write(model, out)
        content = out.read_text(encoding="utf-8")
        assert "# Titre MD" in content
        assert "## Une section" in content
        assert "| A |" in content
        assert "- Note" in content

    def test_escape_pipe_in_cell(self, tmp_path: Path) -> None:
        """Les pipes sont échappés dans les cellules."""
        section = {
            "section_code": "s",
            "title": "S",
            "narrative_blocks": [],
            "tables": [
                {
                    "caption": "c",
                    "headers": ["H"],
                    "rows": [["a|b"]],
                }
            ],
            "insights": [],
        }
        model = ReportModel("t", "T", "a", "b", [], [section])
        out = tmp_path / "p.md"
        MarkdownWriter().write(model, out)
        assert r"a\|b" in out.read_text(encoding="utf-8")

    def test_write_raises_on_invalid_path(self, tmp_path: Path) -> None:
        """Erreur d'écriture encapsulée dans WriterError."""
        blocker = tmp_path / "f"
        blocker.write_text("", encoding="utf-8")
        model = ReportModel("t", "T", "a", "b", [], [])
        with pytest.raises(WriterError, match="Markdown"):
            MarkdownWriter().write(model, blocker / "x.md")
