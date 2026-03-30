"""Module contenant la définition structurelle d'un type de rapport."""

from baobab_activity_reporting.exceptions.report_generation_error import (
    ReportGenerationError,
)


class ReportDefinition:
    """Décrit les sections et prérequis KPI d'un rapport métier.

    Chaque section est un triplet ``(code, titre affiché, préfixes KPI)``.
    La section est éligible si au moins un enregistrement KPI présent dans
    le :class:`ReportContext` a un ``code`` commençant par l'un des préfixes
    (comparaison sensible à la casse). Si l'ensemble des préfixes est vide,
    la section est toujours considérée comme éligible côté données.

    :param report_type: Identifiant logique du rapport (ex. ``activity_phone``).
    :type report_type: str
    :param title_template: Modèle de titre global ; utiliser les placeholders
        ``{period_start}`` et ``{period_end}`` (dates ISO).
    :type title_template: str
    :param sections: Sections ordonnées : ``(code, titre, frozenset[préfixes])``.
    :type sections: tuple[tuple[str, str, frozenset[str]], ...]

    :raises ReportGenerationError: Si ``report_type`` ou ``sections`` est vide.

    :Example:
        >>> from baobab_activity_reporting.reporting.report_definition import (
        ...     ReportDefinition,
        ... )
        >>> d = ReportDefinition.activity_telephony()
        >>> d.report_type
        'activity_telephony'
    """

    def __init__(
        self,
        report_type: str,
        title_template: str,
        sections: tuple[tuple[str, str, frozenset[str]], ...],
    ) -> None:
        """Initialise une définition de rapport.

        :param report_type: Type logique du rapport.
        :type report_type: str
        :param title_template: Modèle de titre avec ``{period_start}`` /
            ``{period_end}``.
        :type title_template: str
        :param sections: Définition ordonnée des sections.
        :type sections: tuple[tuple[str, str, frozenset[str]], ...]
        :raises ReportGenerationError: Si la définition est invalide.
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
        if len(sections) == 0:
            raise ReportGenerationError(
                "Au moins une section est requise dans la définition",
                report_type=report_type,
            )
        self.report_type: str = report_type.strip()
        self.title_template: str = title_template.strip()
        self._sections: tuple[tuple[str, str, frozenset[str]], ...] = sections

    @property
    def sections(self) -> tuple[tuple[str, str, frozenset[str]], ...]:
        """Sections ordonnées du rapport.

        :return: Triplets ``(code, titre section, préfixes KPI requis)``.
        :rtype: tuple[tuple[str, str, frozenset[str]], ...]
        """
        return self._sections

    @classmethod
    def activity_telephony(cls) -> "ReportDefinition":
        """Définition du rapport synthèse téléphonique et canaux tickets.

        :return: Définition prête à planifier.
        :rtype: ReportDefinition
        """
        return cls(
            report_type="activity_telephony",
            title_template="Activité téléphonique — du {period_start} au {period_end}",
            sections=(
                (
                    "telephony_overview",
                    "Synthèse téléphonique",
                    frozenset({"telephony."}),
                ),
                (
                    "ticket_channels",
                    "Répartition des tickets par canal",
                    frozenset({"tickets.channel."}),
                ),
            ),
        )

    @classmethod
    def activity_by_site(cls) -> "ReportDefinition":
        """Définition du rapport d'activité agrégée par site.

        :return: Définition prête à planifier.
        :rtype: ReportDefinition
        """
        return cls(
            report_type="activity_by_site",
            title_template="Activité par site — du {period_start} au {period_end}",
            sections=(
                (
                    "site_breakdown",
                    "Indicateurs par site",
                    frozenset({"site."}),
                ),
            ),
        )

    @classmethod
    def activity_by_agent(cls) -> "ReportDefinition":
        """Définition du rapport d'activité par agent.

        :return: Définition prête à planifier.
        :rtype: ReportDefinition
        """
        return cls(
            report_type="activity_by_agent",
            title_template="Activité par agent — du {period_start} au {period_end}",
            sections=(
                (
                    "agent_breakdown",
                    "Indicateurs par agent",
                    frozenset({"agent."}),
                ),
            ),
        )

    def __repr__(self) -> str:
        """Représentation technique.

        :return: Représentation.
        :rtype: str
        """
        return (
            f"ReportDefinition(report_type={self.report_type!r}, "
            f"sections_count={len(self._sections)})"
        )
