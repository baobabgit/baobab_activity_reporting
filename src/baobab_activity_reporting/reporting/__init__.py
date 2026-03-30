"""Planification éditoriale et construction du modèle de rapport."""

from baobab_activity_reporting.reporting.insight_builder import InsightBuilder
from baobab_activity_reporting.reporting.narrative_builder import NarrativeBuilder
from baobab_activity_reporting.reporting.report_builder import ReportBuilder
from baobab_activity_reporting.reporting.report_context import ReportContext
from baobab_activity_reporting.reporting.report_definition import ReportDefinition
from baobab_activity_reporting.reporting.report_model import ReportModel
from baobab_activity_reporting.reporting.report_planner import ReportPlanner
from baobab_activity_reporting.reporting.section_eligibility_evaluator import (
    SectionEligibilityEvaluator,
)
from baobab_activity_reporting.reporting.table_builder import TableBuilder
from baobab_activity_reporting.reporting.writers.abstract_writer import AbstractWriter
from baobab_activity_reporting.reporting.writers.docx_writer import DocxWriter
from baobab_activity_reporting.reporting.writers.markdown_writer import (
    MarkdownWriter,
)

__all__: list[str] = [
    "AbstractWriter",
    "DocxWriter",
    "InsightBuilder",
    "NarrativeBuilder",
    "ReportBuilder",
    "ReportContext",
    "ReportDefinition",
    "ReportModel",
    "ReportPlanner",
    "SectionEligibilityEvaluator",
    "MarkdownWriter",
    "TableBuilder",
]
