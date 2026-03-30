# baobab-activity-reporting

API Python de reporting d'activité pour Baobab.

## Description

Ce projet fournit une API Python capable de :

1. extraire des données issues de plusieurs fichiers sources ;
2. nettoyer, normaliser et valider ces données ;
3. appliquer des règles métier pour relier les données entre elles ;
4. calculer des indicateurs d'activité (agrégations par période, site, agent,
   canal, pipeline `KpiComputationPipeline`) ;
5. stocker les données calculées ;
6. planifier et construire un modèle éditorial (`ReportModel`) à partir des KPI,
   sans dépendance au format de sortie — voir `docs/report_types.md` ;
7. exporter ce modèle vers des formats documentaires (DOCX, Markdown) ;
8. orchestrer l’ensemble via une façade applicative (`ReportingService`) et une CLI.

## Installation

### Prérequis

- Python 3.10 ou supérieur

### Installation en mode développement

```bash
pip install -e ".[dev]"
```

## Utilisation

```python
from baobab_activity_reporting import PackageMetadata

meta = PackageMetadata()
print(meta.summary())
```

### Calcul des KPI (données préparées en SQLite)

Les indicateurs sont calculés à partir des tables préparées
(`appels_entrants`, `appels_sortants`, `tickets`) et stockés dans `kpi_data`.
Voir `docs/kpi_metrics_catalog.md` pour la liste des codes produits.

```python
from datetime import date

from baobab_activity_reporting import KpiComputationPipeline, ReportingPeriod
from baobab_activity_reporting.storage.repositories.kpi_repository import (
    KpiRepository,
)
from baobab_activity_reporting.storage.repositories.prepared_data_repository import (
    PreparedDataRepository,
)
from baobab_activity_reporting.storage.sqlite.database_session_manager import (
    DatabaseSessionManager,
)

manager = DatabaseSessionManager("reporting.db")
try:
    prepared = PreparedDataRepository(manager)
    kpis = KpiRepository(manager)
    period = ReportingPeriod(date(2026, 1, 1), date(2026, 1, 31))
    pipeline = KpiComputationPipeline(
        prepared,
        kpis,
        period,
        clear_existing_for_period=True,
    )
    summary = pipeline.run()
    print(summary)
finally:
    manager.close()
```

### Modèle de rapport (planification et construction)

À partir des enregistrements KPI (même schéma que `KpiRepository.load_all()`),
le moteur éditorial exclut les sections sans données, puis produit titres,
narratifs, tableaux et insights.

```python
from datetime import date

from baobab_activity_reporting import (
    ReportBuilder,
    ReportContext,
    ReportDefinition,
    ReportingPeriod,
)

period = ReportingPeriod(date(2026, 1, 1), date(2026, 1, 31))
kpi_rows = [
    {"code": "telephony.incoming.count", "label": "Entrants", "value": 10.0,
     "unit": "appels"},
]
context = ReportContext(period, kpi_rows)
model = ReportBuilder().build(ReportDefinition.activity_telephony(), context)
document = model.to_document_tree()
```

### Export DOCX et Markdown

Les writers ne contiennent que la mise en forme fichier. Détails et limites :
`docs/document_writers.md`.

```python
from pathlib import Path

from baobab_activity_reporting import DocxWriter, MarkdownWriter

DocxWriter().write(model, Path("rapport.docx"))
MarkdownWriter().write(model, Path("rapport.md"))
```

### Façade applicative et chaîne complète

Les cas d’usage `ImportSourcesUseCase`, `ComputeMetricsUseCase` et
`GenerateReportUseCase` enrobent respectivement l’ingestion CSV → SQLite,
le `KpiComputationPipeline` et le `ReportBuilder` (+ writers optionnels).
`ReportingService` les expose avec une seule session SQLite.

Guide pas à pas : `docs/end_to_end_pipeline.md`.

```python
from datetime import date

from baobab_activity_reporting import (
    ReportDefinition,
    ReportingPeriod,
    ReportingService,
)

service = ReportingService("reporting.db")
try:
    service.import_sources("incoming.csv", "outgoing.csv", "tickets.csv")
    period = ReportingPeriod(date(2026, 3, 1), date(2026, 3, 31))
    service.compute_metrics(period, clear_existing_for_period=True)
    model = service.generate_report(
        period,
        ReportDefinition.activity_telephony(),
        markdown_path="rapport.md",
    )
finally:
    service.close()
```

### Interface en ligne de commande

Après installation du package, la commande `baobab-reporting` enregistre les
trois étapes (`import`, `compute`, `generate`). Exemple :

```bash
baobab-reporting --log-level INFO import \
  --database reporting.db \
  --incoming data/incoming.csv \
  --outgoing data/outgoing.csv \
  --tickets data/tickets.csv
```

```bash
baobab-reporting compute --database reporting.db \
  --period-start 2026-03-01 --period-end 2026-03-31 --clear-period
```

```bash
baobab-reporting generate --database reporting.db \
  --period-start 2026-03-01 --period-end 2026-03-31 \
  --report-type activity_telephony --markdown rapport.md
```

Les sous-commandes émettent du JSON sur la sortie standard (résumés ou
métadonnées du rapport).

## Outils de qualité

Le projet utilise les outils suivants, tous configurés dans `pyproject.toml` :

| Outil   | Rôle                          |
|---------|-------------------------------|
| black   | Formatage automatique         |
| pylint  | Analyse statique              |
| flake8  | Vérification PEP 8            |
| mypy    | Vérification des types        |
| bandit  | Détection de vulnérabilités   |
| pytest  | Exécution des tests           |
| coverage| Couverture de code            |

### Lancer les vérifications

```bash
black --check src/ tests/
pylint src/
flake8 src/ tests/
mypy src/
bandit -r src/ -c pyproject.toml
pytest
```

## Structure du projet

```
src/
  baobab_activity_reporting/
    __init__.py
    core/
      __init__.py
      package_metadata.py
    application/
      __init__.py
      compute_metrics_use_case.py
      generate_report_use_case.py
      import_sources_use_case.py
      report_definition_resolver.py
      reporting_service.py
    cli/
      __init__.py
      main.py
    domain/
      __init__.py
      models/
        __init__.py
        agent.py
        kpi.py
        reporting_period.py
        site.py
      results/
        __init__.py
        data_availability.py
        extraction_result.py
        section_decision.py
        validation_result.py
    exceptions/
      __init__.py
      application_exception.py
      configuration_exception.py
      extraction_error.py
      persistence_error.py
      report_generation_error.py
      reporting_error.py
      resolution_error.py
      standardization_error.py
      validation_error.py
      writer_error.py
    ingestion/
      __init__.py
      extractors/
        __init__.py
        base_extractor.py
        csv_extraction_configuration.py
        csv_incoming_calls_extractor.py
        csv_outgoing_calls_extractor.py
        csv_ticket_extractor.py
    processing/
      __init__.py
      cleaning/
        __init__.py
        data_cleaner.py
      normalization/
        __init__.py
        column_mapper.py
        data_type_normalizer.py
        standardization_pipeline.py
        value_standardizer.py
      validation/
        __init__.py
        dataset_validator.py
        schema_registry.py
        validation_rule.py
      kpi/
        __init__.py
        activity_aggregator.py
        agent_kpi_calculator.py
        consolidated_data_schema.py
        kpi_computation_pipeline.py
        period_aggregator.py
        site_kpi_calculator.py
        telephony_kpi_calculator.py
    reporting/
      __init__.py
      insight_builder.py
      narrative_builder.py
      report_builder.py
      report_context.py
      report_definition.py
      report_model.py
      report_planner.py
      section_eligibility_evaluator.py
      table_builder.py
      writers/
        __init__.py
        abstract_writer.py
        docx_writer.py
        markdown_writer.py
    storage/
      __init__.py
      sqlite/
        __init__.py
        database_session_manager.py
      repositories/
        __init__.py
        raw_data_repository.py
        prepared_data_repository.py
        kpi_repository.py
        report_data_repository.py
tests/
  conftest.py
  fixtures/
    incoming_calls.csv
    outgoing_calls.csv
    tickets.csv
    empty.csv
    malformed.csv
  baobab_activity_reporting/
    application/
      test_compute_metrics_use_case.py
      test_generate_report_use_case.py
      test_import_sources_use_case.py
      test_report_definition_resolver.py
      test_reporting_service.py
    cli/
      test_main.py
    core/
      test_package_metadata.py
    domain/
      models/
        test_agent.py
        test_kpi.py
        test_reporting_period.py
        test_site.py
      results/
        test_data_availability.py
        test_extraction_result.py
        test_section_decision.py
        test_validation_result.py
    exceptions/
      test_application_exception.py
      test_kpi_computation_error.py
      test_configuration_exception.py
      test_extraction_error.py
      test_persistence_error.py
      test_report_generation_error.py
      test_reporting_error.py
      test_resolution_error.py
      test_standardization_error.py
      test_validation_error.py
      test_writer_error.py
    ingestion/
      extractors/
        test_base_extractor.py
        test_csv_extraction_configuration.py
        test_csv_incoming_calls_extractor.py
        test_csv_outgoing_calls_extractor.py
        test_csv_ticket_extractor.py
    processing/
      cleaning/
        test_data_cleaner.py
      kpi/
        test_activity_aggregator.py
        test_agent_kpi_calculator.py
        test_kpi_computation_pipeline.py
        test_period_aggregator.py
        test_site_kpi_calculator.py
        test_telephony_kpi_calculator.py
      reporting/
        writers/
          test_abstract_writer.py
          test_docx_writer.py
          test_markdown_writer.py
          test_writers_integration.py
        test_insight_builder.py
        test_narrative_builder.py
        test_report_builder.py
        test_report_context.py
        test_report_definition.py
        test_report_model.py
        test_report_planner.py
        test_section_eligibility_evaluator.py
        test_table_builder.py
      normalization/
        test_column_mapper.py
        test_data_type_normalizer.py
        test_standardization_pipeline.py
        test_value_standardizer.py
      validation/
        test_dataset_validator.py
        test_schema_registry.py
        test_validation_rule.py
    reporting/
      writers/
        test_abstract_writer.py
        test_docx_writer.py
        test_markdown_writer.py
        test_writers_integration.py
      test_insight_builder.py
      test_narrative_builder.py
      test_report_builder.py
      test_report_context.py
      test_report_definition.py
      test_report_model.py
      test_report_planner.py
      test_section_eligibility_evaluator.py
      test_table_builder.py
    storage/
      sqlite/
        test_database_session_manager.py
      repositories/
        test_raw_data_repository.py
        test_prepared_data_repository.py
        test_kpi_repository.py
        test_report_data_repository.py
docs/
  dev_diary.md
  document_writers.md
  end_to_end_pipeline.md
  kpi_metrics_catalog.md
  report_types.md
  tests/
    coverage/
```

## Versioning

Ce projet suit le [Semantic Versioning](https://semver.org/) (SemVer).

## Licence

MIT
