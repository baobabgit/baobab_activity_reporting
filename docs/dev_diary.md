# Journal de développement — baobab-activity-reporting

## 2026-03-26 15:45:00

### Modifications

- Création du sous-package `storage/sqlite/` avec `DatabaseSessionManager` :
  gestion de connexion SQLite, initialisation automatique du schéma (4 tables),
  mode WAL, fermeture propre, support `:memory:` et fichier.
- Création du sous-package `storage/repositories/` avec :
  - `RawDataRepository` : persistance des données brutes (save/load/count/delete).
  - `PreparedDataRepository` : persistance des données nettoyées/normalisées.
  - `KpiRepository` : persistance des indicateurs calculés avec période.
  - `ReportDataRepository` : persistance des sections de rapport générées.
- Schéma SQLite minimal : `raw_data`, `prepared_data`, `kpi_data`, `report_data`.
- Sérialisation JSON des lignes DataFrame pour le stockage row-level.
- Ajout de 43 tests unitaires sur base SQLite en mémoire (`:memory:`).
- Configuration bandit : skip B608 (f-strings avec noms de tables constantes).
- Passage en version 0.5.0.

### Buts

- Mettre en place une couche de persistance abstraite adossée à SQLite,
  séparant données brutes, préparées et métriques.
- Permettre le stockage intermédiaire entre les étapes du pipeline pour
  faciliter l'audit, le recalcul et la traçabilité.

### Impact

- Les données extraites, standardisées et les KPI calculés peuvent
  désormais être persistés en SQLite et relus.
- Toute erreur SQLite est encapsulée dans `PersistenceError`.
- Le domaine ne dépend pas directement des détails SQLite : les
  repositories abstraient l'accès aux données.
- La couverture de code reste à 97 %.

## 2026-03-26 14:15:00

### Modifications

- Création du sous-package `processing/normalization/` avec :
  - `ColumnMapper` : renommage de colonnes via un dictionnaire de mapping.
  - `DataTypeNormalizer` : conversion de colonnes vers datetime, int, float.
  - `ValueStandardizer` : normalisation des valeurs textuelles (espaces,
    accents, casse) pour harmoniser les libellés d'agents et de sites.
  - `StandardizationPipeline` : orchestrateur enchaînant mapping, nettoyage,
    normalisation des types et standardisation des valeurs.
- Création du sous-package `processing/cleaning/` avec :
  - `DataCleaner` : strip des espaces, normalisation de casse (lower, upper,
    title) sur les colonnes texte.
- Création du sous-package `processing/validation/` avec :
  - `ValidationRule` : règle abstraite applicable à un DataFrame.
  - `ColumnPresenceRule` : vérifie la présence de colonnes obligatoires.
  - `NullRatioRule` : vérifie le taux de valeurs nulles par colonne.
  - `SchemaRegistry` : registre de schémas attendus par type de source,
    générant automatiquement les règles de validation.
  - `DatasetValidator` : exécute séquentiellement les règles et agrège
    les résultats dans un `ValidationResult`.
- Ajout de 75 tests unitaires pour la standardisation et la validation.
- Passage en version 0.4.0.

### Buts

- Rendre les données extraites homogènes, typées et exploitables
  avant toute règle de rapprochement métier.
- Permettre la détection précoce d'anomalies structurelles et de qualité.

### Impact

- Les données issues des extracteurs CSV peuvent maintenant être
  nettoyées, renommées, typées et validées de manière systématique.
- Les erreurs de conversion sont encapsulées dans `StandardizationError`.
- Les contrôles de validation distinguent erreurs bloquantes et
  avertissements via `ValidationResult`.
- La couverture de code reste à 100 %.

## 2026-03-26 11:10:00

### Modifications

- Création du sous-package `ingestion/extractors/` pour la couche d'ingestion.
- Création de `CsvExtractionConfiguration` : objet de configuration de lecture
  CSV (séparateur, encodage, colonnes attendues, lignes à ignorer, libellé).
- Création de `BaseExtractor` : extracteur abstrait implémentant la lecture
  CSV via pandas, la vérification d'existence du fichier, la détection des
  colonnes manquantes et la journalisation via `logging`.
- Création de `CsvIncomingCallsExtractor` : extracteur spécialisé pour les
  fichiers d'appels entrants avec colonnes attendues prédéfinies.
- Création de `CsvOutgoingCallsExtractor` : extracteur spécialisé pour les
  fichiers d'appels sortants.
- Création de `CsvTicketExtractor` : extracteur spécialisé pour les fichiers
  de tickets (EFI, EDI, téléphone).
- Ajout de `pandas>=2.1.0,<3.0.0` comme dépendance de production et
  `pandas-stubs>=2.1.0` comme dépendance de développement.
- Création de fixtures CSV de test dans `tests/fixtures/` (appels entrants,
  appels sortants, tickets, fichier vide, fichier malformé, colonnes
  manquantes).
- Création de `tests/conftest.py` avec la fixture `fixtures_dir`.
- Ajout de 35 tests unitaires couvrant toutes les classes d'ingestion.
- Désactivation de `duplicate-code` dans pylint (similarité structurelle
  attendue entre extracteurs).
- Mise à jour de `README.md`, `CHANGELOG.md` et passage en version 0.3.0.

### Buts

- Fournir une couche d'ingestion propre capable de lire les fichiers CSV
  métiers en renvoyant des résultats d'extraction structurés.
- Séparer strictement la lecture de fichier de toute logique métier.
- Permettre aux features suivantes (standardisation, validation) de
  s'appuyer sur des `ExtractionResult` fiables.

### Impact

- Les fichiers CSV d'appels entrants, sortants et de tickets peuvent
  être lus avec des extracteurs spécialisés.
- Toute erreur de lecture (fichier absent, encodage invalide, etc.) est
  encapsulée dans une `ExtractionError` du projet.
- Les colonnes manquantes sont signalées en warning sans bloquer
  l'extraction.
- La couverture de code reste à 100 %.

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
