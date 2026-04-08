"""Résolution du type de rapport vers :class:`ReportDefinition`."""

from baobab_activity_reporting.exceptions.configuration_exception import (
    ConfigurationException,
)
from baobab_activity_reporting.reporting.report_definition import ReportDefinition


def resolve_report_definition(report_type: str) -> ReportDefinition:
    """Retourne la définition de rapport pour un identifiant logique.

    :param report_type: Identifiant (ex. ``activity_telephony``).
    :type report_type: str
    :return: Définition prête pour :class:`GenerateReportUseCase`.
    :rtype: ReportDefinition
    :raises ConfigurationException: Si ``report_type`` est inconnu.
    """
    key = report_type.strip()
    registry: dict[str, ReportDefinition] = {
        "activity_telephony": ReportDefinition.activity_telephony(),
        "activity_by_site": ReportDefinition.activity_by_site(),
        "activity_by_agent": ReportDefinition.activity_by_agent(),
        "weekly_activity_by_agent": ReportDefinition.weekly_activity_by_agent(),
        "weekly_activity_by_site": ReportDefinition.weekly_activity_by_site(),
    }
    if key not in registry:
        raise ConfigurationException(
            "Type de rapport inconnu",
            parameter_name="report_type",
            details=f"valeur: {report_type!r}, attendu un de: {sorted(registry)}",
        )
    return registry[key]
