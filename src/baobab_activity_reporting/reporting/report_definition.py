"""Module contenant la définition structurelle d'un type de rapport."""

import importlib
from typing import cast

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


def _editorial_from_legacy(
    section_code: str,
    section_title: str,
    kpi_prefixes: frozenset[str],
) -> EditorialSectionDefinition:
    """Construit une section éditoriale minimale depuis l'ancien triplet.

    :param section_code: Code de section.
    :type section_code: str
    :param section_title: Titre affiché.
    :type section_title: str
    :param kpi_prefixes: Préfixes KPI pour la porte de visibilité.
    :type kpi_prefixes: frozenset[str]
    :return: Définition éditoriale par défaut.
    :rtype: EditorialSectionDefinition
    """
    return EditorialSectionDefinition(
        section_code=section_code,
        section_title=section_title,
        section_objective="",
        required_data=frozenset(),
        optional_data=frozenset(),
        display_rules=DisplayRules.default(),
        writing_style=WritingStyle.default(),
        visibility_rule=SectionVisibilityRule.from_prefixes(
            kpi_prefixes,
            mandatory_in_report=False,
        ),
        table_policy=TablePolicy.default(),
    )


class ReportDefinition:
    """Décrit un rapport métier comme une suite de sections éditoriales.

    Chaque section porte objectifs, jeux de données attendus, règles d'affichage
    et règle de visibilité (préfixes KPI, obligation, retrait).

    :param report_type: Identifiant logique du rapport.
    :type report_type: str
    :param title_template: Modèle de titre ; placeholders ``{period_start}``,
        ``{period_end}``.
    :type title_template: str
    :param editorial_sections: Sections ordonnées du plan éditorial.
    :type editorial_sections: tuple[EditorialSectionDefinition, ...]

    :raises ReportGenerationError: Si la définition est invalide.

    :Example:
        >>> d = ReportDefinition.activity_telephony()
        >>> d.report_type
        'activity_telephony'
    """

    def __init__(
        self,
        report_type: str,
        title_template: str,
        editorial_sections: tuple[EditorialSectionDefinition, ...],
    ) -> None:
        """Initialise une définition de rapport.

        :param report_type: Type logique du rapport.
        :type report_type: str
        :param title_template: Modèle de titre.
        :type title_template: str
        :param editorial_sections: Sections du plan.
        :type editorial_sections: tuple[EditorialSectionDefinition, ...]
        :raises ReportGenerationError: Si paramètres invalides.
        """
        if not report_type.strip():
            raise ReportGenerationError(
                "Le type de rapport ne peut pas être vide",
                report_type=report_type,
            )
        if not title_template.strip():
            raise ReportGenerationError(
                "Le modèle de titre ne peut pas être vide",
                report_type=report_type,
            )
        if len(editorial_sections) == 0:
            raise ReportGenerationError(
                "Au moins une section est requise dans la définition",
                report_type=report_type,
            )
        self.report_type: str = report_type.strip()
        self.title_template: str = title_template.strip()
        self._editorial_sections: tuple[EditorialSectionDefinition, ...] = editorial_sections

    @property
    def editorial_sections(self) -> tuple[EditorialSectionDefinition, ...]:
        """Sections éditoriales ordonnées.

        :return: Tuple immuable des sections.
        :rtype: tuple[EditorialSectionDefinition, ...]
        """
        return self._editorial_sections

    @property
    def sections(self) -> tuple[tuple[str, str, frozenset[str]], ...]:
        """Vue legacy ``(code, titre, préfixes KPI)`` pour compatibilité.

        :return: Triplets dérivés des règles de visibilité.
        :rtype: tuple[tuple[str, str, frozenset[str]], ...]
        """
        return tuple(s.legacy_triplet() for s in self._editorial_sections)

    @classmethod
    def activity_telephony(cls) -> "ReportDefinition":
        """Rapport synthèse téléphonique et canaux tickets.

        :return: Définition prête à planifier.
        :rtype: ReportDefinition
        """
        sections = (
            _editorial_from_legacy(
                "telephony_overview",
                "Synthèse téléphonique",
                frozenset({"telephony."}),
            ),
            _editorial_from_legacy(
                "ticket_channels",
                "Répartition des tickets par canal",
                frozenset({"tickets.channel."}),
            ),
        )
        return cls(
            report_type="activity_telephony",
            title_template="Activité téléphonique — du {period_start} au {period_end}",
            editorial_sections=sections,
        )

    @classmethod
    def activity_by_site(cls) -> "ReportDefinition":
        """Rapport d'activité agrégée par site.

        :return: Définition prête à planifier.
        :rtype: ReportDefinition
        """
        return cls(
            report_type="activity_by_site",
            title_template="Activité par site — du {period_start} au {period_end}",
            editorial_sections=(
                _editorial_from_legacy(
                    "site_breakdown",
                    "Indicateurs par site",
                    frozenset({"site."}),
                ),
            ),
        )

    @classmethod
    def activity_by_agent(cls) -> "ReportDefinition":
        """Rapport d'activité par agent.

        :return: Définition prête à planifier.
        :rtype: ReportDefinition
        """
        return cls(
            report_type="activity_by_agent",
            title_template="Activité par agent — du {period_start} au {period_end}",
            editorial_sections=(
                _editorial_from_legacy(
                    "agent_breakdown",
                    "Indicateurs par agent",
                    frozenset({"agent."}),
                ),
            ),
        )

    @classmethod
    def weekly_activity_by_agent(cls) -> "ReportDefinition":
        """Rapport hebdomadaire structuré par plan éditorial (focus agent).

        :return: Définition hebdomadaire agent.
        :rtype: ReportDefinition
        """
        mod = importlib.import_module(
            "baobab_activity_reporting.reporting.weekly_activity_by_agent_report_definition",
        )
        built = mod.WeeklyActivityByAgentReportDefinition.build()
        return cast(ReportDefinition, built)

    @classmethod
    def weekly_activity_by_site(cls) -> "ReportDefinition":
        """Rapport hebdomadaire structuré par plan éditorial (focus site).

        :return: Définition hebdomadaire site.
        :rtype: ReportDefinition
        """
        mod = importlib.import_module(
            "baobab_activity_reporting.reporting.weekly_activity_by_site_report_definition",
        )
        built = mod.WeeklyActivityBySiteReportDefinition.build()
        return cast(ReportDefinition, built)

    def __repr__(self) -> str:
        """Représentation technique.

        :return: Représentation.
        :rtype: str
        """
        return (
            f"ReportDefinition(report_type={self.report_type!r}, "
            f"sections_count={len(self._editorial_sections)})"
        )
