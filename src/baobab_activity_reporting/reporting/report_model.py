"""Module du modèle de rapport indépendant du format de sortie."""

from typing import Any, Mapping


class ReportModel:
    """Représente le contenu éditorial structuré d'un rapport d'activité.

    Les sections sont des dictionnaires sérialisables (titres, narratifs,
    tableaux, insights) sans aucune dépendance à un format DOCX, Markdown
    ou HTML.

    :param report_type: Identifiant du type de rapport.
    :type report_type: str
    :param title: Titre principal affichable.
    :type title: str
    :param period_start: Début de période ISO.
    :type period_start: str
    :param period_end: Fin de période ISO.
    :type period_end: str
    :param preamble_narratives: Textes liminaires (ex. introduction globale).
    :type preamble_narratives: list[str]
    :param sections: Contenu par section (structure libre mais documentée).
    :type sections: list[dict[str, object]]

    :Example:
        >>> m = ReportModel("t", "T", "2026-01-01", "2026-01-31", [], [])
        >>> m.report_type
        't'
    """

    def __init__(
        self,
        report_type: str,
        title: str,
        period_start: str,
        period_end: str,
        preamble_narratives: list[str],
        sections: list[dict[str, object]],
    ) -> None:
        """Initialise le modèle de rapport.

        :param report_type: Type logique.
        :type report_type: str
        :param title: Titre du document.
        :type title: str
        :param period_start: Borne de début.
        :type period_start: str
        :param period_end: Borne de fin.
        :type period_end: str
        :param preamble_narratives: Introduction(s).
        :type preamble_narratives: list[str]
        :param sections: Sections construites.
        :type sections: list[dict[str, object]]
        """
        self.report_type: str = report_type
        self.title: str = title
        self.period_start: str = period_start
        self.period_end: str = period_end
        self.preamble_narratives: list[str] = list(preamble_narratives)
        self.sections: list[dict[str, object]] = list(sections)

    @property
    def section_codes(self) -> list[str]:
        """Codes des sections présentes dans le modèle.

        :return: Ordre de construction.
        :rtype: list[str]
        """
        codes: list[str] = []
        for block in self.sections:
            raw = block.get("section_code")
            if raw is not None:
                codes.append(str(raw))
        return codes

    def to_document_tree(self) -> dict[str, object]:
        """Expose une arborescence prête pour une couche de rendu.

        :return: Carte imbriquée reprenant toutes les clés publiques.
        :rtype: dict[str, object]
        """
        cloned_sections: list[dict[str, object]] = []
        for section in self.sections:
            cloned_sections.append(self._shallow_clone_mapping(section))
        return {
            "report_type": self.report_type,
            "title": self.title,
            "period_start": self.period_start,
            "period_end": self.period_end,
            "preamble_narratives": list(self.preamble_narratives),
            "sections": cloned_sections,
        }

    @staticmethod
    def _shallow_clone_mapping(section: Mapping[str, object]) -> dict[str, object]:
        """Duplique un bloc section pour export sans alias partagés.

        :param section: Mapping source.
        :type section: Mapping[str, object]
        :return: Nouveau dictionnaire.
        :rtype: dict[str, object]
        """
        result: dict[str, object] = {}
        for key, val in section.items():
            if isinstance(val, list):
                result[str(key)] = list(val)
            elif isinstance(val, dict):
                nested: dict[str, Any] = dict(val)
                result[str(key)] = nested
            else:
                result[str(key)] = val
        return result
