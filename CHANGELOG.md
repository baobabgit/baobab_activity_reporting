# Changelog

Tous les changements notables de ce projet seront documentés dans ce fichier.

Le format suit [Keep a Changelog](https://keepachangelog.com/fr/1.1.0/)
et ce projet adhère au [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.3.0] - 2026-03-26

### Added

- Couche d'ingestion avec sous-package `ingestion/extractors/`.
- `CsvExtractionConfiguration` : configuration de lecture CSV (séparateur,
  encodage, colonnes attendues, skip_rows, source_label).
- `BaseExtractor` : extracteur abstrait avec lecture CSV, gestion d'erreurs
  et journalisation.
- `CsvIncomingCallsExtractor` : extracteur spécialisé appels entrants.
- `CsvOutgoingCallsExtractor` : extracteur spécialisé appels sortants.
- `CsvTicketExtractor` : extracteur spécialisé tickets.
- Fixtures de test CSV réalistes dans `tests/fixtures/`.
- `conftest.py` avec fixture `fixtures_dir` partagée.
- Dépendance de production `pandas>=2.1.0,<3.0.0`.
- Dépendance de développement `pandas-stubs>=2.1.0`.
- 35 nouveaux tests unitaires pour la couche d'ingestion.

## [0.2.0] - 2026-03-26

### Added

- Modèles métier : `ReportingPeriod`, `Agent`, `Site`, `Kpi`.
- Objets de résultat techniques : `ExtractionResult`, `ValidationResult`,
  `SectionDecision`, `DataAvailability`.
- Hiérarchie d'exceptions métier : `ReportingError`, `ExtractionError`,
  `ValidationError`, `StandardizationError`, `ResolutionError`,
  `PersistenceError`, `ReportGenerationError`, `WriterError`.
- Énumérations `Severity` et `SectionStatus`.
- Sous-packages `domain/models/` et `domain/results/`.
- Tests unitaires pour toutes les nouvelles classes (175 nouveaux tests).

## [0.1.0] - 2026-03-26

### Added

- Initialisation du socle projet avec `pyproject.toml`.
- Arborescence `src/baobab_activity_reporting/`, `tests/`, `docs/`.
- Exception de base `ApplicationException`.
- Exception technique `ConfigurationException`.
- Classe `PackageMetadata` pour l'accès aux métadonnées du package.
- Configuration de black, pylint, mypy, flake8, bandit, pytest et coverage.
- Séparation des dépendances de production et de développement.
- Documentation initiale : `README.md`, `CHANGELOG.md`, `docs/dev_diary.md`.
- Tests unitaires des exceptions et de `PackageMetadata`.
