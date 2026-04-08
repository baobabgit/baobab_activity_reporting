"""Définition éditoriale complète d'une section de rapport."""

from __future__ import annotations

from dataclasses import dataclass

from baobab_activity_reporting.exceptions.report_generation_error import (
    ReportGenerationError,
)
from baobab_activity_reporting.reporting.editorial.display_rules import DisplayRules
from baobab_activity_reporting.reporting.editorial.section_visibility_rule import (
    SectionVisibilityRule,
)
from baobab_activity_reporting.reporting.editorial.table_policy import TablePolicy
from baobab_activity_reporting.reporting.editorial.writing_style import WritingStyle


@dataclass(frozen=True, slots=True)
class EditorialSectionDefinition:  # pylint: disable=too-many-instance-attributes
    """Section d'un plan éditorial : objectif, données, style et règles.

    Les identifiants ``required_data`` et ``optional_data`` sont des libellés
    sémantiques stables (ex. ``slot.telephony.global``) pour documenter les
    jeux de données attendus ; le moteur actuel s'appuie surtout sur les
    préfixes KPI de :class:`SectionVisibilityRule`.

    :param section_code: Identifiant technique unique dans le rapport.
    :type section_code: str
    :param section_title: Titre affiché.
    :type section_title: str
    :param section_objective: But rédactionnel de la section.
    :type section_objective: str
    :param required_data: Fentes de données considérées comme requises.
    :type required_data: frozenset[str]
    :param optional_data: Fentes de données optionnelles.
    :type optional_data: frozenset[str]
    :param display_rules: Règles de présentation.
    :type display_rules: DisplayRules
    :param writing_style: Style rédactionnel.
    :type writing_style: WritingStyle
    :param visibility_rule: Règle d'inclusion / retrait.
    :type visibility_rule: SectionVisibilityRule
    :param table_policy: Paramètres des tableaux KPI.
    :type table_policy: TablePolicy

    :raises ReportGenerationError: Si ``section_code`` ou ``section_title``
        est vide après normalisation.
    """

    section_code: str
    section_title: str
    section_objective: str
    required_data: frozenset[str]
    optional_data: frozenset[str]
    display_rules: DisplayRules
    writing_style: WritingStyle
    visibility_rule: SectionVisibilityRule
    table_policy: TablePolicy

    def __post_init__(self) -> None:
        """Valide les champs obligatoires.

        :raises ReportGenerationError: Si code ou titre invalide.
        :rtype: None
        """
        code = self.section_code.strip()
        title = self.section_title.strip()
        if not code:
            raise ReportGenerationError(
                "section_code ne peut pas être vide",
                report_type="editorial_section",
            )
        if not title:
            raise ReportGenerationError(
                "section_title ne peut pas être vide",
                report_type=code,
            )

    def eligibility_prefixes(self) -> frozenset[str]:
        """Préfixes KPI utilisés pour le filtrage (compatibilité planificateur).

        :return: Copie logique des préfixes de la règle de visibilité.
        :rtype: frozenset[str]
        """
        return self.visibility_rule.kpi_prefixes

    def legacy_triplet(self) -> tuple[str, str, frozenset[str]]:
        """Représentation legacy ``(code, titre, préfixes)``.

        :return: Triplet attendu par l'ancien planificateur.
        :rtype: tuple[str, str, frozenset[str]]
        """
        return (
            self.section_code,
            self.section_title,
            self.visibility_rule.kpi_prefixes,
        )
