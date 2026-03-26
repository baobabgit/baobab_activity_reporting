# baobab-activity-reporting

API Python de reporting d'activité pour Baobab.

## Description

Ce projet fournit une API Python capable de :

1. extraire des données issues de plusieurs fichiers sources ;
2. nettoyer, normaliser et valider ces données ;
3. appliquer des règles métier pour relier les données entre elles ;
4. calculer des indicateurs d'activité ;
5. stocker les données calculées ;
6. générer un rapport d'activité structuré et exportable.

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
tests/
  conftest.py
  fixtures/
    incoming_calls.csv
    outgoing_calls.csv
    tickets.csv
    empty.csv
    malformed.csv
  baobab_activity_reporting/
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
docs/
  dev_diary.md
  tests/
    coverage/
```

## Versioning

Ce projet suit le [Semantic Versioning](https://semver.org/) (SemVer).

## Licence

MIT
