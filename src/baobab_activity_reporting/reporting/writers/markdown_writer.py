"""Writer exportant un ReportModel en Markdown (UTF-8)."""

import logging
from pathlib import Path
from typing import Any, Mapping, cast

from baobab_activity_reporting.exceptions.writer_error import WriterError
from baobab_activity_reporting.reporting.report_model import ReportModel
from baobab_activity_reporting.reporting.writers.abstract_writer import (
    AbstractWriter,
)

logger = logging.getLogger(__name__)


class MarkdownWriter(AbstractWriter):
    """Produit un fichier ``.md`` lisible et versionnable.

    Titres, paragraphes, tableaux GFM et listes à puces ; aucune règle
    d'agrégation ou de priorisation métier.

    :Example:
        >>> MarkdownWriter().output_format
        'markdown'
    """

    @property
    def output_format(self) -> str:
        """Format logique ``markdown``.

        :return: Identifiant de format.
        :rtype: str
        """
        return "markdown"

    def write(self, model: ReportModel, output_path: Path | str) -> None:
        """Écrit le Markdown au chemin indiqué.

        :param model: Rapport à exporter.
        :type model: ReportModel
        :param output_path: Fichier ``.md`` cible.
        :type output_path: Path | str
        :raises WriterError: Si l'écriture disque échoue.
        """
        path = Path(output_path)
        try:
            text = self._render_string(model)
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(text, encoding="utf-8", newline="\n")
        except OSError as exc:
            raise WriterError(
                "Impossible d'écrire le fichier Markdown",
                output_format=self.output_format,
                details=str(exc),
            ) from exc
        logger.info("Markdown enregistré : %s", path)

    def _render_string(self, model: ReportModel) -> str:
        """Construit le contenu Markdown complet.

        :param model: Source.
        :type model: ReportModel
        :return: Texte du fichier.
        :rtype: str
        """
        lines: list[str] = []
        lines.append(f"# {self._escape_heading(model.title)}")
        lines.append("")
        lines.append(
            f"*Période : {model.period_start} — {model.period_end}*",
        )
        lines.append("")
        for block in model.preamble_narratives:
            lines.extend(block.splitlines() or [""])
            lines.append("")
        for section in model.sections:
            self._append_section(lines, cast(Mapping[str, Any], section))
        return "\n".join(lines).rstrip() + "\n"

    def _append_section(self, lines: list[str], section: Mapping[str, Any]) -> None:
        """Ajoute une section au flux de lignes.

        :param lines: Accumulateur.
        :type lines: list[str]
        :param section: Bloc section.
        :type section: Mapping[str, Any]
        """
        title = str(section.get("title", section.get("section_code", "Section")))
        lines.append(f"## {self._escape_heading(title)}")
        lines.append("")
        narratives = section.get("narrative_blocks")
        if isinstance(narratives, list):
            for para in narratives:
                lines.extend(str(para).splitlines() or [""])
                lines.append("")
        tables = section.get("tables")
        if isinstance(tables, list):
            for tbl in tables:
                if isinstance(tbl, dict):
                    self._append_table(lines, cast(dict[str, Any], tbl))
        insights = section.get("insights")
        if isinstance(insights, list) and len(insights) > 0:
            lines.append("### Points saillants")
            lines.append("")
            for item in insights:
                lines.append(f"- {self._escape_cell(str(item))}")
            lines.append("")

    def _append_table(self, lines: list[str], table_map: dict[str, Any]) -> None:
        """Ajoute un tableau Markdown (GFM).

        :param lines: Accumulateur.
        :type lines: list[str]
        :param table_map: Dict ``caption`` / ``headers`` / ``rows``.
        :type table_map: dict[str, Any]
        """
        caption = table_map.get("caption")
        if caption is not None:
            lines.append(f"**{self._escape_cell(str(caption))}**")
            lines.append("")
        headers = table_map.get("headers")
        rows = table_map.get("rows")
        if not isinstance(headers, list) or len(headers) == 0:
            return
        if not isinstance(rows, list):
            return
        esc_headers = [self._escape_cell(str(h)) for h in headers]
        lines.append("| " + " | ".join(esc_headers) + " |")
        lines.append("| " + " | ".join(["---"] * len(esc_headers)) + " |")
        for row in rows:
            if isinstance(row, (list, tuple)):
                cells = [
                    self._escape_cell(str(row[i] if i < len(row) else ""))
                    for i in range(len(headers))
                ]
            else:
                cells = [""] * len(headers)
            lines.append("| " + " | ".join(cells) + " |")
        lines.append("")

    @staticmethod
    def _escape_heading(text: str) -> str:
        """Évite les ambiguïtés de titre Markdown minimales.

        :param text: Titre brut.
        :type text: str
        :return: Titre inchangé (pas de préfixe ``#`` interne attendu).
        :rtype: str
        """
        return text.replace("\n", " ").strip()

    @staticmethod
    def _escape_cell(text: str) -> str:
        """Échappe les pipes pour les cellules de tableau.

        :param text: Cellule.
        :type text: str
        :return: Texte sûr pour une ligne GFM.
        :rtype: str
        """
        return text.replace("|", "\\|").replace("\n", " ")
