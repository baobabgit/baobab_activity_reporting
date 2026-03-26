# Journal de développement — baobab-activity-reporting

## 2026-03-26 10:15:00

### Modifications

- Création du sous-package `domain/models/` contenant `ReportingPeriod`, `Agent`,
  `Site` et `Kpi`.
- Création du sous-package `domain/results/` contenant `ExtractionResult`,
  `ValidationResult` (avec `Severity` et `ValidationMessage`), `SectionDecision`
  (avec `SectionStatus`) et `DataAvailability`.
- Création de la hiérarchie d'exceptions métier : `ReportingError` (parente
  directe de `ApplicationException`) puis `ExtractionError`, `ValidationError`,
  `StandardizationError`, `ResolutionError`, `PersistenceError`,
  `ReportGenerationError` et `WriterError`.
- Mise à jour des exports dans tous les `__init__.py` du package racine,
  de `exceptions/`, `domain/models/` et `domain/results/`.
- Ajout de 175 tests unitaires couvrant toutes les nouvelles classes.
- Mise à jour de `README.md`, `CHANGELOG.md` et passage en version 0.2.0.
- Ajustement de pylint (`max-args`, `max-positional-arguments`) dans
  `pyproject.toml` pour autoriser 6 paramètres.

### Buts

- Poser le vocabulaire métier et technique du projet pour découpler le
  domaine des `DataFrame`.
- Standardiser la gestion des erreurs avec une hiérarchie d'exceptions
  cohérente couvrant chaque couche du pipeline.

### Impact

- Chaque couche du pipeline (extraction, standardisation, validation,
  résolution, persistance, génération de rapport, rendu) dispose
  désormais de sa propre exception dédiée.
- Les modèles métier (`Agent`, `Site`, `Kpi`, `ReportingPeriod`)
  permettent de manipuler des objets typés plutôt que des `DataFrame`.
- Les objets de résultat (`ExtractionResult`, `ValidationResult`,
  `SectionDecision`, `DataAvailability`) standardisent le transport
  des métadonnées entre les couches.
- La couverture de code reste à 100 %.

## 2026-03-26 09:00:00

### Modifications

- Création de l'arborescence du projet : `src/baobab_activity_reporting/`, `tests/`, `docs/`.
- Création du fichier `pyproject.toml` avec toute la configuration centralisée.
- Ajout des dépendances de production (aucune pour l'instant) et de développement
  (black, pylint, mypy, flake8, Flake8-pyproject, bandit, pytest, pytest-cov, coverage).
- Création de la classe `ApplicationException` : exception de base du projet.
- Création de la classe `ConfigurationException` : exception technique héritant
  de `ApplicationException`.
- Création de la classe `PackageMetadata` : accès centralisé au nom et à la version
  du package.
- Création des fichiers `__init__.py` avec les exports publics.
- Création du `README.md`, du `CHANGELOG.md` et de ce journal de développement.
- Création des tests unitaires pour les trois classes.

### Buts

- Mettre en place le socle du projet : dépôt installable, ossature du package,
  outils de qualité, base documentaire, hiérarchie d'exceptions racine.
- Permettre à toute feature future de s'appuyer sur une base saine et testée.

### Impact

- Le package est installable via `pip install -e ".[dev]"`.
- Les outils de qualité (black, pylint, mypy, flake8, bandit) sont configurés
  et opérationnels.
- La couverture de code est mesurée et ses rapports sont générés dans
  `docs/tests/coverage`.
- La hiérarchie d'exceptions est en place : toute exception future du projet
  héritera de `ApplicationException`.
- `PackageMetadata` centralise l'accès aux métadonnées du package.
