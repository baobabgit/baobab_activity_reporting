"""Module de construction des blocs narratifs."""

from baobab_activity_reporting.reporting.report_context import ReportContext


class NarrativeBuilder:
    """Produit des paragraphes descriptifs à partir du contexte et des KPI.

    Le contenu est en français et ne contient aucune balise de format
    documentaire : uniquement du texte brut prêt à être injecté dans un
    moteur de rendu ultérieur.

    :Example:
        >>> from datetime import date
        >>> from baobab_activity_reporting.domain.models.reporting_period import (
        ...     ReportingPeriod,
        ... )
        >>> from baobab_activity_reporting.reporting.report_context import (
        ...     ReportContext,
        ... )
        >>> from baobab_activity_reporting.reporting.narrative_builder import (
        ...     NarrativeBuilder,
        ... )
        >>> p = ReportingPeriod(date(2026, 1, 1), date(2026, 1, 31))
        >>> ctx = ReportContext(p, [])
        >>> NarrativeBuilder().lead_paragraph(ctx, "Titre")
        'Ce rapport couvre la période du 2026-01-01 au 2026-01-31.'
    """

    def lead_paragraph(self, context: ReportContext, report_title: str) -> str:
        """Génère une phrase d'introduction pour tout le rapport.

        :param context: Période couverte.
        :type context: ReportContext
        :param report_title: Titre déjà formaté du rapport.
        :type report_title: str
        :return: Paragraphe d'accroche.
        :rtype: str
        """
        _ = report_title
        start, end = context.period_iso_bounds()
        return (
            f"Ce rapport couvre la période du {start} au {end}. "
            f"{self._kpi_count_sentence(context)}"
        )

    def section_intro(
        self,
        section_code: str,
        section_title: str,
        kpi_count: int,
    ) -> str:
        """Introduit une section à partir de son identifiant et du volume de KPI.

        :param section_code: Code technique de la section.
        :type section_code: str
        :param section_title: Titre lisible.
        :type section_title: str
        :param kpi_count: Nombre d'indicateurs dans la section.
        :type kpi_count: int
        :return: Court paragraphe introductif.
        :rtype: str
        """
        _ = section_code
        if kpi_count == 0:
            return f"La section « {section_title} » ne contient aucun indicateur."
        if kpi_count == 1:
            return (
                f"La section « {section_title} » s'appuie sur un indicateur clé "
                "pour cette période."
            )
        return (
            f"La section « {section_title} » présente {kpi_count} indicateurs "
            "pour cette période."
        )

    @staticmethod
    def _kpi_count_sentence(context: ReportContext) -> str:
        """Phrase sur le nombre total de KPI.

        :param context: Contexte source.
        :type context: ReportContext
        :return: Phrase complémentaire.
        :rtype: str
        """
        total = len(context.kpi_records)
        if total == 0:
            return "Aucun indicateur n'est disponible pour cette période."
        if total == 1:
            return "Un indicateur agrège l'activité sur cette période."
        return f"{total} indicateurs agrègent l'activité sur cette période."
